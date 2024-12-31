from setuptools import setup

APP = ['main.py']  
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'ffmpeg-python'],  
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'ffmpeg-python'],
    'iconfile': 'icon.ico',  
}
