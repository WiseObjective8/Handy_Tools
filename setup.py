'''Youtube Setup'''
from setuptools import setup, find_packages

setup(
    name='Youtube',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List any dependencies here, e.g.,
        'pytubefix', 'ffmpeg-python', 'PyQt5'
    ],
    entry_points={
        'console_scripts': [
            'yt-cli=Youtube.cli:main',  # If you have a CLI entry point in cli.py
        ],
    },
)
