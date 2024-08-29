import sys
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import (
    QThreadPool,
    QSize, 
    Qt, 
    QRect, 
    QFileInfo, 
    QFile, 
    QDir, 
    QUrl
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
)
from Youtube.gui_helpers import show_alert, DownloadWorker
from Youtube.logic_helpers import APP_PATH


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set up the UI
        self.setWindowTitle("Youtube Downloader")
        self.resize(549, 390)
        self.setMinimumSize(QSize(549, 390))
        self.setMaximumSize(QSize(549, 390))
        self.setFocusPolicy(Qt.TabFocus)
        self.setAutoFillBackground(False)

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QRect(10, 0, 527, 386))

        self.central_layout = QVBoxLayout(self.layoutWidget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.url_layout = QHBoxLayout()
        self.url_label = QLabel("URL", self.layoutWidget)
        self.url_input = QLineEdit(self.layoutWidget)
        self.url_layout.addWidget(self.url_label)
        self.url_layout.addWidget(self.url_input)
        self.central_layout.addLayout(self.url_layout)

        self.th_files_layout = QHBoxLayout()
        self.bar_layout = QVBoxLayout()
        self.thumbnail = QGraphicsView(self.layoutWidget)
        self.bar_layout.addWidget(self.thumbnail)

        self.options_layout = QHBoxLayout()
        self.play_vid_layout = QVBoxLayout()
        self.video_check = QRadioButton("Video", self.layoutWidget)
        self.playlist_check = QRadioButton("Playlist", self.layoutWidget)
        self.play_vid_layout.addWidget(self.video_check)
        self.play_vid_layout.addWidget(self.playlist_check)
        self.options_layout.addLayout(self.play_vid_layout)

        self.type_layout = QVBoxLayout()
        self.mp3 = QCheckBox("MP3", self.layoutWidget)
        self.mp4 = QCheckBox("MP4", self.layoutWidget)
        self.merged = QCheckBox("Merged", self.layoutWidget)
        self.type_layout.addWidget(self.mp3)
        self.type_layout.addWidget(self.mp4)
        self.type_layout.addWidget(self.merged)
        self.options_layout.addLayout(self.type_layout)

        self.res_layout = QVBoxLayout()
        self._480p = QCheckBox("480p", self.layoutWidget)
        self._720p = QCheckBox("720p", self.layoutWidget)
        self._1080p = QCheckBox("1080p", self.layoutWidget)
        self.res_layout.addWidget(self._480p)
        self.res_layout.addWidget(self._720p)
        self.res_layout.addWidget(self._1080p)
        self.options_layout.addLayout(self.res_layout)

        self.bar_layout.addLayout(self.options_layout)

        self.progressBar = QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(Qt.Horizontal)
        self.bar_layout.addWidget(self.progressBar)

        self.th_files_layout.addLayout(self.bar_layout)

        self.file_view = QTreeView(self.layoutWidget)
        self.th_files_layout.addWidget(self.file_view)

        self.central_layout.addLayout(self.th_files_layout)

        self.buttons_layout = QHBoxLayout()
        self.download_btn = QPushButton("Download", self.layoutWidget)
        self.open_file_btn = QPushButton("Open", self.layoutWidget)
        self.del_file_btn = QPushButton("Delete", self.layoutWidget)
        self.close_btn = QPushButton("Close", self.layoutWidget)

        self.buttons_layout.addWidget(self.download_btn)
        self.buttons_layout.addWidget(self.open_file_btn)
        self.buttons_layout.addWidget(self.del_file_btn)
        self.buttons_layout.addWidget(self.close_btn)

        self.central_layout.addLayout(self.buttons_layout)

        # Set up file view
        self.model = QFileSystemModel()
        self.model.setRootPath(APP_PATH)
        self.file_view.setModel(self.model)
        self.file_view.setRootIndex(self.model.index(APP_PATH))
        self.file_view.clicked.connect(self.on_clicked)

        # Set up thread pool
        self.thread_pool = QThreadPool()

        # Connect buttons
        self.download_btn.clicked.connect(self.start_download)
        self.open_file_btn.clicked.connect(self.open_selected)
        self.del_file_btn.clicked.connect(self.delete_selected)
        self.close_btn.clicked.connect(self.close)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            show_alert("Please enter a valid URL.")
            return

        is_playlist = self.playlist_check.isChecked()
        if not (self.video_check.isChecked() or is_playlist):
            show_alert("Please select 'Video' or 'Playlist'.")
            return

        file_type = (
            3
            if self.mp3.isChecked() and self.mp4.isChecked()
            else (1 if self.mp3.isChecked() else 2 if self.mp4.isChecked() else 3)
        )
        resolution = (
            3 if self._480p.isChecked() else 2 if self._720p.isChecked() else 1
        )

        # Create worker and connect the completion signal
        worker = DownloadWorker(url, is_playlist, file_type, resolution)
        worker.signals.completed.connect(show_alert)
        self.thread_pool.start(worker)

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
                # QMessageBox.information(
                #     self, "Deleted", f"'{self.selected_path}' has been deleted."
                # )
                self.file_view.setRootIndex(self.model.index(APP_PATH))

    def on_clicked(self, index):
        self.selected_path = self.model.filePath(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
