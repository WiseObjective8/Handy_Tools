import os
import shutil
import re
from typing import Union, Dict
from pytubefix import Playlist
from Youtube.errors import (
    InvalidURLError,
    DirectoryCreationError,
    DownloadError,
    FailedDirectoryEmptyError,
)
from Youtube.yt_vid_logic import YT
from Youtube.logic_helpers import APP_PATH, handle_errors, sanitize_filename


class PL(Playlist):
    def __init__(
        self,
        url: str,
        app_path: str = APP_PATH,
        client: str = "WEB",
        proxies: Union[Dict[str, str], None] = None,
        use_oauth: bool = False,
        allow_oauth_cache: bool = True,
        token_file: Union[str, None] = None,
    ):
        super().__init__(url, client, proxies, use_oauth, allow_oauth_cache, token_file)
        self.video_handle = YT
        self.app_path = app_path
        self._title = sanitize_filename(self.title)
        self.path = f"{self.app_path}\\{self._title}"
        self.tmp = f"{self.app_path}\\{self._title}\\tmp"
        self.thumbnail_url = None  # self.video_handle.thumbnail_url
        self.thumbnail_list = []
        self._create_directories()

    def _create_directories(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp, exist_ok=True)

    def download_video(self, _type: int, resolution: Union[None, int] = None):
        if not self.video_urls:
            raise DownloadError("No video URLs found in the playlist.")
        for i in self.video_urls:
            
            self.video_handle(i, app_path=self.path).download_video(_type, resolution)
            print(i)
            # downloader = self.video_handle(i, app_path=self.path)
            # self.thumbnail_url = downloader.get_thumbnail_url()[0]
            # downloader.download_video(_type, resolution)
        self.empty_folder(self.tmp)

    def get_thumbnail_url(self):
        return [self.video_handle(i).thumbnail_url for i in self.video_urls]

    def empty_folder(self, path: str) -> None:
        if os.path.exists(path):
            shutil.rmtree(path)
