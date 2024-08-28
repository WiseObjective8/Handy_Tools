# pylint: disable = missing-function-docstring
# pylint: disable = missing-class-docstring
# pylint: disable = broad-exception-caught
import sys
import os
from typing import Union
# pylint: disable = no-name-in-module
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QPushButton,
    QButtonGroup,
    QMessageBox,
    QCheckBox,
)
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot, pyqtSignal, QObject
from Youtube.yt_vid_logic import YT
from Youtube.yt_playlist_logic import PL
from Youtube.logic_helpers import APP_PATH


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


class DownloaderGUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__path = APP_PATH
        self.thread_pool = QThreadPool()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 400)
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # URL input layout
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)

        # Type selection layout
        type_layout = QHBoxLayout()
        self.radio_video = QRadioButton("Video")
        self.radio_playlist = QRadioButton("Playlist")
        type_group = QButtonGroup(self)
        type_group.addButton(self.radio_video)
        type_group.addButton(self.radio_playlist)
        type_layout.addWidget(self.radio_video)
        type_layout.addWidget(self.radio_playlist)

        # File format options layout
        options_layout = QHBoxLayout()
        self.audio_check = QCheckBox("MP3")
        self.video_check = QCheckBox("MP4")
        options_layout.addWidget(self.audio_check)
        options_layout.addWidget(self.video_check)

        # Resolution selection layout
        format_layout = QHBoxLayout()
        self.res_1080p = QRadioButton("1080p")
        self.res_720p = QRadioButton("720p")
        self.res_480p = QRadioButton("480p")
        format_layout.addWidget(self.res_1080p)
        format_layout.addWidget(self.res_720p)
        format_layout.addWidget(self.res_480p)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.download_button = QPushButton("Download")
        self.show_button = QPushButton("Show")
        buttons_layout.addWidget(self.download_button)
        buttons_layout.addWidget(self.show_button)

        # Adding layouts to the main layout
        layout.addLayout(url_layout)
        layout.addLayout(type_layout)
        layout.addLayout(options_layout)
        layout.addLayout(format_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connecting signals to slots
        self.download_button.clicked.connect(self.start_download)
        self.show_button.clicked.connect(self.show_files)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            show_alert("Please enter a valid URL.")
            return

        is_playlist = self.radio_playlist.isChecked()
        if not (self.radio_video.isChecked() or is_playlist):
            show_alert("Please select 'Video' or 'Playlist'.")
            return

        file_type = (
            3
            if self.audio_check.isChecked() and self.video_check.isChecked()
            else (
                1
                if self.audio_check.isChecked()
                else 2 if self.video_check.isChecked() else 3
            )
        )
        resolution = (
            3 if self.res_480p.isChecked() else 2 if self.res_720p.isChecked() else 1
        )

        # Create worker and connect the completion signal
        worker = DownloadWorker(url, is_playlist, file_type, resolution)
        worker.signals.completed.connect(show_alert)
        self.thread_pool.start(worker)

    def show_files(self):
        try:
            if sys.platform == "win32":
                os.startfile(self.__path)
            elif sys.platform == "darwin":
                os.system(f"open {self.__path}")
            else:
                os.system(f"xdg-open {self.__path}")
        except Exception as e:
            show_alert(f"{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader_gui = DownloaderGUI()
    downloader_gui.show()
    sys.exit(app.exec_())
