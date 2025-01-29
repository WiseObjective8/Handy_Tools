import sys
import urllib.request
from PyQt5.QtGui import QDesktopServices, QPixmap, QIcon
from PyQt5.QtCore import (
    QThreadPool,
    QSize,
    Qt,
    QRect,
    QFileInfo,
    QFile,
    QDir,
    QUrl,
    QTimer,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox,
    QRadioButton,
    QProgressBar,
    QLabel,
    QLineEdit,
    QWidget,
    QGraphicsView,
    QPushButton,
    QTreeView,
    QFileSystemModel,
    QMessageBox,
    QGraphicsScene,
    QSizePolicy,
)
from Youtube.gui_helpers import show_alert, DownloadWorker
from Youtube.logic_helpers import handle_errors
from Youtube.logic_helpers import APP_PATH, url_check
import urllib

ICON_PATH = "./icons/default.svg"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowTitle("Youtube Downloader")
        self.setMinimumSize(QSize(566, 418))
        self.setMaximumSize(QSize(566 * 2, 418))  # Double of initial size for maximum

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        self.central_layout.setSpacing(10)

        self.url_layout = QHBoxLayout()
        self.url_label = QLabel("URL", self.centralwidget)
        self.url_input = QLineEdit(self.centralwidget)
        self.url_input.setMinimumWidth(200)
        self.url_layout.addWidget(self.url_label)
        self.url_layout.addWidget(self.url_input)
        self.central_layout.addLayout(self.url_layout)

        self.th_files_layout = QHBoxLayout()
        self.bar_layout = QVBoxLayout()

        self.thumbnail = QLabel(self.centralwidget)
        self.thumbnail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.thumbnail.setAlignment(Qt.AlignCenter)

        self.bar_layout.addWidget(self.thumbnail)

        self.options_layout = QHBoxLayout()
        self.type_layout = QVBoxLayout()
        self.mp3 = QCheckBox("MP3", self.centralwidget)
        self.mp4 = QCheckBox("MP4", self.centralwidget)
        self.merged = QCheckBox("Merged", self.centralwidget)
        self.type_layout.addWidget(self.mp3)
        self.type_layout.addWidget(self.mp4)
        self.type_layout.addWidget(self.merged)
        self.options_layout.addLayout(self.type_layout)

        self.res_layout = QVBoxLayout()
        self._480p = QCheckBox("480p", self.centralwidget)
        self._720p = QCheckBox("720p", self.centralwidget)
        self._1080p = QCheckBox("1080p", self.centralwidget)
        self.res_layout.addWidget(self._480p)
        self.res_layout.addWidget(self._720p)
        self.res_layout.addWidget(self._1080p)
        self.options_layout.addLayout(self.res_layout)

        self.bar_layout.addLayout(self.options_layout)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setMinimumHeight(20)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.bar_layout.addWidget(self.progressBar)

        self.th_files_layout.addLayout(self.bar_layout)
        self.file_view = QTreeView(self.centralwidget)
        self.file_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.th_files_layout.addWidget(self.file_view)
        self.central_layout.addLayout(self.th_files_layout)

        self.buttons_layout = QHBoxLayout()
        self.download_btn = QPushButton("Download", self.centralwidget)
        self.open_file_btn = QPushButton("Open", self.centralwidget)
        self.del_file_btn = QPushButton("Delete", self.centralwidget)
        self.close_btn = QPushButton("Close", self.centralwidget)
        self.buttons_layout.addWidget(self.download_btn)
        self.buttons_layout.addWidget(self.open_file_btn)
        self.buttons_layout.addWidget(self.del_file_btn)
        self.buttons_layout.addWidget(self.close_btn)
        self.central_layout.addLayout(self.buttons_layout)

        self.model = QFileSystemModel()
        self.model.setRootPath(APP_PATH)
        self.file_view.setModel(self.model)
        self.file_view.setRootIndex(self.model.index(APP_PATH))
        self.file_view.clicked.connect(self.on_clicked)
        self.thread_pool = QThreadPool()
        self.download_btn.clicked.connect(self.start_download)
        self.open_file_btn.clicked.connect(self.open_selected)
        self.del_file_btn.clicked.connect(self.delete_selected)
        self.close_btn.clicked.connect(self.close)
        self._pixmap = QPixmap()
        self._pixmap.load(ICON_PATH)
        self._resized_pixmap = self._pixmap.scaled(self.thumbnail.size())
        self.thumbnail.setPixmap(self._pixmap)
        self.thumbnail.setStyleSheet("border: 2px solid white;")
        self.thumbnail.show()
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.print_window_size)
        # self.timer.start(1000)  # 1000 milliseconds = 1 second

    def print_window_size(self):
        size = self.size()
        print(f"Window Size: {size.width()} x {size.height()}")

    def start_download(self):
        url = self.url_input.text().strip()
        x = url_check(url)
        if type(x) is not int:
            show_alert("Please enter a valid URL.")

            return
        else:
            is_playlist = x == 1
        file_type = {
            1: self.mp3.isChecked(),
            2: self.mp4.isChecked(),
            3: self.merged.isChecked(),
        }
        resolution = {
            1: self._480p.isChecked(),
            2: self._720p.isChecked(),
            3: self._1080p.isChecked(),
        }
        if file_type == {1: True, 2: False, 3: False}:
            resolution = {k: False for k in resolution}
        worker = DownloadWorker(url, is_playlist, file_type, resolution)
        worker.signals.thumbnail.connect(self.update_thumbnail)
        self.thread_pool.start(worker)
        worker.signals.completed.connect(show_alert)

    def update_thumbnail(self, thumbnail_url):
        print(thumbnail_url)
        try:
            print(f"Loading thumbnail from URL: {thumbnail_url}")

            if (
                thumbnail_url
                and isinstance(thumbnail_url, str)
                and thumbnail_url.strip()
            ):
                response = urllib.request.urlopen(thumbnail_url)
                data = response.read()
                self._pixmap.loadFromData(data)
                print(f"Thumbnail loaded: {thumbnail_url}")
            else:
                raise ValueError("None")

        except ValueError as ve:
            print(f"ValueError encountered: {ve}. Loading default thumbnail.")
            self._pixmap.load("./icons/default.png")

        except Exception as e:
            print(f"Error loading thumbnail: {e}. Loading default thumbnail.")
            self._pixmap.load("./icons/default.png")

        self._resized_pixmap = self._pixmap.scaled(
            self.thumbnail.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        self.thumbnail.setPixmap(self._resized_pixmap)
        self.thumbnail.setStyleSheet("border: 2px solid white;")
        self.thumbnail.show()

    def open_selected(self):
        if hasattr(self, "selected_path") and QFileInfo(self.selected_path).isFile():
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.selected_path))

    def delete_selected(self):
        if hasattr(self, "selected_path"):
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete '{self.selected_path}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                if QFileInfo(self.selected_path).isDir():
                    QDir(self.selected_path).removeRecursively()
                else:
                    QFile.remove(self.selected_path)
                self.file_view.setRootIndex(self.model.index(APP_PATH))

    def on_clicked(self, index):
        self.selected_path = self.model.filePath(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
