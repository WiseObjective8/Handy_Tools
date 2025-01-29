import urllib.request
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from typing import Union
from Youtube.yt_vid_logic import YT
from Youtube.yt_playlist_logic import PL
import urllib

def show_alert(msg: Union[str, None] = None):
    alert = QMessageBox()
    alert.setWindowTitle("Alert")
    alert.setText(msg)
    alert.setIcon(QMessageBox.Information)
    alert.setStandardButtons(QMessageBox.Ok)
    alert.exec_()


class WorkerSignals(QObject):
    completed = pyqtSignal(str)
    thumbnail = pyqtSignal(str)  # New signal to emit the thumbnail URL


class DownloadWorker(QRunnable):
    def __init__(
        self,
        url: str,
        is_playlist: bool,
        file_type: dict[int, bool],
        resolution: dict[int, bool],
    ):
        super().__init__()
        self.url = url
        self.is_playlist = is_playlist
        self.file_type = file_type
        self.resolution = resolution
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            handler = PL if self.is_playlist else YT
            downloader = handler(self.url)
            __type = (
                list(self.file_type.values()) if any(self.resolution.items()) else 1
            )
            if __type != 1:
                for k, v in self.resolution.items():
                    if t := __type[k - 1]:
                        print(f"This is from {self.__class__.__name__}: {downloader.thumbnail_url}")
                        self.signals.thumbnail.emit(downloader.thumbnail_url)
                        downloader.download_video(__type.index(t) + 1, v)
                        
            else:
                print(f"This is from {self.__class__.__name__}: {downloader.thumbnail_url}")
                self.signals.thumbnail.emit(*downloader.thumbnail_url)
                downloader.download_video(__type)


            self.signals.completed.emit(f"{downloader.title} is downloaded")
        except Exception as e:
            self.signals.completed.emit(f"{str(e)}")


# - Emerald Green: #50C878
# - Sapphire Blue: #0F52BA
# - Icy Blue: #B2FFFF
# - Bright Pink: #FF007F
# - Black: #000000
# - White: #FFFFFF
# - Navy: #000080