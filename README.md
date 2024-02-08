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