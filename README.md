Here's the `README.md` in English:

```markdown
# Video to Audio Converter

## Introduction
**Video to Audio Converter** is a simple application that converts video files to MP3 audio files using the `ffmpeg` library in Python. The app provides a graphical user interface (GUI) using `PyQt5`, allowing users to select a video file, convert it to audio, and save it in a desired location.

## Features
- Convert video files (MP4, AVI, MKV, MOV) to MP3 audio files.
- Interactive GUI using `PyQt5`.
- Ability to choose the destination folder for the output file.

## Requirements
Before you can run the application, make sure you have the following dependencies installed:

### 1. **Python 3.x**
You need Python 3.x installed on your machine.

### 2. **ffmpeg**
You need to install `ffmpeg` to process and convert video files to audio. You can install `ffmpeg` using [Homebrew](https://brew.sh/) on macOS:

```bash
brew install ffmpeg
```

### 3. **Required Libraries**
Make sure you've installed the following libraries using `pip`:

```bash
pip install ffmpeg-python PyQt5
```

## Running the Application

### 1. **Run the Application Directly**
After installing the dependencies, you can run the application with the following command in the terminal:

```bash
python main.py
```

A window will open where you can select the video file to convert it to an MP3 audio file.

### 2. **Choose Output Folder**
You can choose the destination folder where you want to save the converted audio file.

### 3. **Progress Display**
During the conversion process, the application will display the progress on the graphical interface.

## Packaging the App for Distribution

If you want to distribute the app as a standalone `.app` file on macOS or an executable on Windows, you can use tools like `py2app` or `PyInstaller` to create standalone executables.

### Steps to Use `py2app` on macOS:

1. First, make sure you have `py2app` installed:

   ```bash
   pip install py2app
   ```

2. Then create a `setup.py` file as follows:

   ```python
   from setuptools import setup

   APP = ['main.py']
   DATA_FILES = []
   OPTIONS = {
       'argv_emulation': True,
       'packages': ['ffmpeg', 'PyQt5'],
   }

   setup(
       app=APP,
       data_files=DATA_FILES,
       options={'py2app': OPTIONS},
       setup_requires=['py2app'],
   )
   ```

3. To package the app, run the following command:

   ```bash
   python setup.py py2app
   ```

This will create the `.app` file in the `dist/` folder.

### Steps to Use `PyInstaller` on Windows/Linux:

1. First, make sure you have `PyInstaller` installed:

   ```bash
   pip install pyinstaller
   ```

2. Then run the following command to generate a standalone executable:

   ```bash
   pyinstaller --onefile main.py
   ```

This will create the executable file in the `dist/` folder.

## Contributing
If you'd like to contribute to this project, feel free to open an [Issue](https://github.com/username/repository/issues) or submit a Pull Request with your changes.

## Developer
This application was developed by **Obaid Bouslahi**.

## License
This project is licensed under the [MIT License](LICENSE).
```

### Explanation of the sections in the `README.md`:
- **Introduction**: Describes the purpose of the application.
- **Features**: Lists key features of the application.
- **Requirements**: Lists the dependencies needed to run the app, such as Python, ffmpeg, and required libraries.
- **Running the Application**: Provides instructions on how to run the app.
- **Packaging the App for Distribution**: Explains how to package the app as a standalone executable using `py2app` (macOS) or `PyInstaller` (Windows/Linux).
- **Contributing**: Encourages others to contribute to the project.
- **Developer**: Credits the developer.
- **License**: States the license under which the project is distributed (MIT License in this case).

Make sure to update the `username/repository` part with your actual GitHub username and repository name and adjust the license link as necessary.