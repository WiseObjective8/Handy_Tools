"""
A class that extends the Playlist functionality for managing and downloading video playlists.
Args:
    url (str): The URL of the playlist to download.
    app_path (str): The base path for storing downloaded content.
    client (str, optional): The client _type for the download. Defaults to "WEB".
    proxies (Dict[str, str] | None, optional): A dictionary of proxy settings to use for the connection.
    use_oauth (bool, optional): Whether to use OAuth for authentication. Defaults to False.
    allow_oauth_cache (bool, optional): Whether to allow caching of OAuth tokens. Defaults to True.
    token_file (str | None, optional): The file path to store the OAuth token.
Methods:
    _create_directories: Creates necessary directories for storing downloads.
    download_playlist: Downloads videos from the playlist based on specified _type and resolution.
    _extract_links: Extracts video URLs from the playlist.
    empty_folder: Removes all files and subdirectories in the specified folder.
"""

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
from Youtube.logs import log_setup
from Youtube.yt_vid_logic import YT
from Youtube.logic_helpers import APP_PATH, handle_errors, sanitize_filename

log_setup()


class PL(Playlist):
    """
    Plalist Logic
    """

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
        self.regex = r"(?:http|https|)(?::\/\/|)(?:www.|)(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/ytscreeningroom\?v=|\/feeds\/api\/videos\/|\/user\S*[^\w\-\s]|\S*[^\w\-\s]))([\w\-]{12,})[a-z0-9;:@#?&%=+\/\$_.-]*"
        if not re.match(self.regex, url):
            raise InvalidURLError
        self.video_handle = YT
        self.app_path = app_path
        self._title = sanitize_filename(self.title)
        self.path = f"{self.app_path}\\{self._title}"
        self.tmp = f"{self.app_path}\\{self._title}\\tmp"
        self._create_directories()

    @handle_errors(DirectoryCreationError)
    def _create_directories(self):
        """
        Create necessary directories for storing downloads if they do not exist.

        This method ensures that the main directory (`self.path`) and the tmp directory (`self.tmp`)
        are created if they do not already exist.
        It handles any errors related to directory creation.
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp, exist_ok=True)

    @handle_errors(DownloadError)
    def download_playlist(self, _type: int, resolution: int = None):
        """
        Download all videos in a playlist.

        This method iterates over the list of video URLs in the playlist and downloads each video
        according to the specified _type and resolution.
        After all videos are downloaded, the tmp directory is emptied.

        Args:
            _type (int): The _type of download (1: audio, 2: video, 3: both).
            resolution (int): The resolution of the video to download (1: 1080p, 2: 720p, 3: 480p).
        """
        for i in self.video_urls:
            self.video_handle(i, app_path=self.path).download_video(_type, resolution)
        self.empty_folder(self.tmp)

    @handle_errors(FailedDirectoryEmptyError)
    def empty_folder(self, path: str) -> None:
        """
        Remove all files and subdirectories in the specified folder.

        :param path: Path to the folder to be emptied.
        """
        if os.path.exists(path):
            shutil.rmtree(path)  # Remove the folder and its contents
