# A OCR tool for converting any image copied to clipboard (including windows snip) to text
* Install pytesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki).
* Make sure pytesseract is installed at ``C:\Program Files\Tesseract-OCR\``.
* Add ``C:\Program Files\Tesseract-OCR\tesseract.exe`` to your PATH
* Add ``parent\directory\OCR\dist\ocr.exe`` to your PATH.
## Usage
- Copy any image with text or snip the area on screen with text.
- Press ``Win + R``
- Type ``ocr.exe`` and hit enter.
- Wait for a terminal to pop-up and close.
- ``Ctrl + V`` for the text in image.
## Note
- This only works on windows, with python 2.5+ and 3.x.
- I used ``pyinstaller`` to generate the executables for ``ocr.py``. 

# OCR Clipboard Tool

This Python script allows you to perform OCR (Optical Character Recognition) on images copied to your clipboard. The recognized text is automatically copied to the clipboard for easy pasting.

## Features

- Automatically detects if an image is available in the clipboard.
- Performs OCR on the image using Tesseract OCR.
- Copies the recognized text to the clipboard for easy access.

## Requirements

- Python 3.7+
- `pytesseract`
- `Pillow` (PIL)
- `pyperclip`
- `numpy`
- `pywin32`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/wiseobjective8/ocr-clipboard-tool.git
    cd ocr-clipboard-tool
    ```

2. Install the required Python packages:

    ```bash
    pip install pytesseract pillow pyperclip numpy pywin32
    ```

3. Ensure Tesseract OCR is installed on your system. You can download it from [tesseract-ocr.github.io](https://tesseract-ocr.github.io/).

4. Update the `tess` parameter in the `OCR` class initialization if Tesseract is installed in a different location:

    ```python
    tess: str = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    ```

## Usage

Simply run the script:

```bash
python your_script.py
```

If an image is available in the clipboard, the script will perform OCR on it and copy the recognized text back to the clipboard.

## Example

1. Copy an image containing text to your clipboard.
2. Run the script:

    ```bash
    python your_script.py
    ```

3. The recognized text will be copied to your clipboard, and you can paste it anywhere.

# YouTube Video Downloader

This Python script allows you to download YouTube videos in various formats and resolutions using the `pytubefix` library. You can choose to download audio, video, or both, and select the resolution of the video.

## Features

- Download audio-only, video-only, or both audio and video from YouTube.
- Choose between different resolutions (1080p, 720p, 480p) for video downloads.
- Automatically handles temporary files and cleans up after downloads.
- Logs download activities to a file and displays messages in the console.

## Requirements

- Python 3.7+
- `pytubefix`
- `ffmpeg`
- `argparse`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/wiseobjective8/yt-downloader.git
    cd yt-downloader
    ```

2. Install the required Python packages:

    ```bash
    pip install pytubefix ffmpeg-python
    ```

3. Ensure `ffmpeg` is installed on your system. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

## Usage

Run the script using the following command:

```bash
python your_script.py --link <YouTube-video-URL>
```

You can also provide multiple URLs separated by spaces:

```bash
python your_script.py --link <YouTube-video-URL1> <YouTube-video-URL2>
```

Alternatively, you can run the script without the `--link` argument and input the video URL(s) interactively.

### Command-Line Arguments

- `--link`: One or more YouTube video URLs to download.

## Interactive Prompts

The script will prompt you to choose:

1. The download type:
    - 1: Audio only
    - 2: Video only
    - 3: Both audio and video (default)

2. The resolution (if downloading video):
    - 1: 1080p (default)
    - 2: 720p
    - 3: 480p

3. A confirmation to proceed with the download.

## Logging

The script logs its activities to a file named `download_log.log` in the current directory. It also prints log messages to the console.

## Packaging as a Standalone Executable

You can create a standalone executable using PyInstaller:

```bash
pyinstaller --onefile --distpath /path/to/your/desired/folder your_script.py
```

Replace `/path/to/your/desired/folder` with the path to the folder where you want the executable to be placed. Add the ```.exe``` to ```PATH``` for global usage of the executable.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for new features.

## License

This project is licensed under the MIT License.
