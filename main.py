import os
import ffmpeg
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class ConvertThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, video_path, output_path):
        super().__init__()
        self.video_path = video_path
        self.output_path = output_path

    def run(self):
        try:
            # Using ffmpeg to convert video to audio and track progress
            process = (
                ffmpeg
                .input(self.video_path)
                .output(self.output_path, format='mp3')
                .global_args('-loglevel', 'info')  # Adjust log level for progress info
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )

            # Reading stderr for progress info
            while True:
                stderr = process.stderr.read(4096).decode('utf-8')
                if not stderr:
                    break
                # Check for progress percentage in stderr
                if 'time=' in stderr:
                    time_str = stderr.split('time=')[1].split(' ')[0]
                    # Convert time format to seconds for the progress
                    hours, minutes, seconds = time_str.split(':')
                    total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                    progress_percentage = (total_seconds / self.get_video_duration()) * 100
                    self.progress.emit(int(progress_percentage))

            process.wait()  # Wait for the process to complete
            self.finished.emit(f"Conversion successful! Saved to: {self.output_path}")

        except ffmpeg.Error as e:
            self.finished.emit(f"An error occurred:\n{e.stderr.decode()}")

    def get_video_duration(self):
        # Get the duration of the video (in seconds) to calculate progress
        probe = ffmpeg.probe(self.video_path, v='error', select_streams='v:0', show_entries='stream=duration')
        return float(probe['streams'][0]['duration'])

class VideoToAudioConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video to Audio Converter")
        self.setGeometry(300, 200, 500, 350)

        # Set up the UI
        self.init_ui()

    def init_ui(self):
        # Create the UI components
        self.label = QLabel("Select a video file to convert to audio", self)
        self.label.setFont(QFont("Arial", 14))
        self.label.setAlignment(Qt.AlignCenter)
        
        self.button = QPushButton("Choose Video", self)
        self.button.setFont(QFont("Arial", 12))
        self.button.clicked.connect(self.select_video)

        self.save_button = QPushButton("Choose Save Location", self)
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.clicked.connect(self.select_save_location)

        self.status_label = QLabel("", self)
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setAlignment(Qt.AlignCenter)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.developer_label = QLabel("Developer: Obaid Bouslahi", self)
        self.developer_label.setFont(QFont("Arial", 8))
        self.developer_label.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.developer_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.video_path = None
        self.output_path = None

    def select_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.video_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "", "Video Files (*.mp4 *.mov *.avi *.mkv)", options=options
        )

        if not self.video_path:
            QMessageBox.warning(self, "No File Selected", "Please select a video file.")
            return

    def select_save_location(self):
        if not self.video_path:
            QMessageBox.warning(self, "No File Selected", "Please select a video file first.")
            return

        # Get the directory of the selected video
        folder = os.path.dirname(self.video_path)

        # Automatically set the output path with the same name as the video, but with an MP3 extension
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        output_path = os.path.join(folder, base_name + ".mp3")

        # Check if the file already exists, and change the name if necessary
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(folder, f"{base_name}_{counter}.mp3")
            counter += 1

        self.output_path = output_path
        self.status_label.setText(f"Output will be saved to: {self.output_path}")
        self.convert_video_to_audio()

    def convert_video_to_audio(self):
        if not self.video_path or not self.output_path:
            QMessageBox.warning(self, "No File or Save Location", "Please select both a video file and a save location.")
            return

        self.status_label.setText("Converting, please wait...")
        self.progress_bar.setValue(0)

        # Create a new thread for the conversion process
        self.thread = ConvertThread(self.video_path, self.output_path)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_conversion_finished)
        self.thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def on_conversion_finished(self, message):
        self.status_label.setText(message)
        if "successful" in message:
            QMessageBox.information(self, "Success", f"Audio file saved at:\n{self.output_path}")
        else:
            QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VideoToAudioConverter()
    window.show()
    sys.exit(app.exec_())
