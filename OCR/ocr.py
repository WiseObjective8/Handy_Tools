import pytesseract
from PIL import Image
import win32clipboard as w
import io
import pyperclip
import numpy as np

class OCR:
    def __init__(self, tess: str = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = tess
        self.snip = None
        self.run()

    def snip_available(self):
        w.OpenClipboard()
        try:
            return w.IsClipboardFormatAvailable(w.CF_DIB)
        finally:
            w.CloseClipboard()

    def get_snip(self):
        w.OpenClipboard()
        try:
            if w.IsClipboardFormatAvailable(w.CF_DIB):
                data = w.GetClipboardData(w.CF_DIB)
                return np.array(Image.open(io.BytesIO(data)))
        finally:
            w.CloseClipboard()
        return None

    def run(self):
        self.snip = self.get_snip()
        if np.any(self.snip):
            self.ocr_image()

    def ocr_image(self):
        text = pytesseract.image_to_string(self.snip)
        pyperclip.copy(text)
        return text


OCR()
