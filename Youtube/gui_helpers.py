from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from typing import Union
from Youtube.yt_vid_logic import YT
from Youtube.yt_playlist_logic import PL

def show_alert(msg: Union[str, None] = None):
    alert = QMessageBox()
    alert.setWindowTitle("Alert")
    alert.setText(msg)
    alert.setIcon(QMessageBox.Information)
    alert.setStandardButtons(QMessageBox.Ok)
    alert.exec_()


class WorkerSignals(QObject):
    completed = pyqtSignal(str)


class DownloadWorker(QRunnable):
    def __init__(self, url: str, is_playlist: bool, file_type: int, resolution: int):
        super().__init__()
        self.url = url
        self.is_playlist = is_playlist
        self.file_type = file_type
        self.resolution = resolution
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            if self.is_playlist:
                downloader = PL(self.url)
                downloader.download_playlist(self.file_type, self.resolution)
            else:
                downloader = YT(self.url)
                downloader.download_video(self.file_type, self.resolution)

            # Emit signal when done
            self.signals.completed.emit(f"{downloader.title} is downloaded")

        except Exception as e:
            self.signals.completed.emit(f"{str(e)}")
