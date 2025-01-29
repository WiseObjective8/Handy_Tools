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

from typing import Callable, Union, Any, Dict
import os
import shutil
import time
import re
import ffmpeg
from pytubefix import YouTube, Stream
from Youtube.errors import (
    _FileExistsError,
    InvalidURLError,
    DirectoryCreationError,
    DownloadError,
    FailedDirectoryEmptyError,
    FFmpegError,
)
from Youtube.logic_helpers import APP_PATH, handle_errors, sanitize_filename

from pytubefix.innertube import _default_clients

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID"]


class YT(YouTube):
    def __init__(
        self,
        url: str,
        app_path: str = APP_PATH,
        client: str = "ANDROID_TESTSUITE",
        on_progress_callback: Union[Callable[[Any, bytes, int], None], None] = None,
        on_complete_callback: Union[
            Callable[[Any, Union[str, None]], None], None
        ] = None,
        proxies: Union[Dict[str, str], None] = None,
        use_oauth: bool = True,
        allow_oauth_cache: bool = True,
        token_file: Union[str, None] = None,
    ):
        super().__init__(
            url,
            client,
            on_progress_callback,
            on_complete_callback,
            proxies,
            use_oauth,
            allow_oauth_cache,
            token_file,
        )
        self.url = url
        self._type = {1: "audio", 2: "video", 3: "both"}
        self.res = {3: "1080p", 2: "720p", 1: "480p"}
        self.t_res = ""
        self.app_path = app_path
        self._title = sanitize_filename(self.title)
        self.tmp = os.path.join(self.app_path, "tmp")
        self._create_directories()
        # print(self.thumbnail_url)

    def get_thumbnail_url(self):
        return list(self.thumbnail_url)

    def _create_directories(self):
        if not os.path.exists(self.app_path):
            os.makedirs(self.app_path, exist_ok=True)
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp, exist_ok=True)

    def download_video(self, _type: int, resolution: Union[int, None] = None):
        self._extract_streams(_type, resolution)
        self.empty_folder(self.tmp)

    def empty_folder(self, path: str) -> None:
        if os.path.exists(path):
            shutil.rmtree(path)

    def _extract_streams(self, _type: int, resolution: Union[int, None] = None):
        self.t_res = self.res.get(resolution, "1080p")
        audio = self.streams.get_audio_only() if _type in {1, 3} else None
        video = self.streams.filter(res=self.t_res).first() if _type in {2, 3} else None
        self._processdata(_type, video, audio)

    def _processdata(self, _type: int, video: Stream = None, audio: Stream = None):
        self.millis = int(time.time() * 1000)
        v_out = os.path.join(self.tmp, f"{self.millis}.mp4")
        a_out = os.path.join(self.tmp, f"{self.millis}.mp3")
        if _type in {2, 3} and video:
            (filename, output_path) = (
                (f"{self._title}_{self.t_res}_video.mp4", self.app_path)
                if _type == 2
                else (f"{self.millis}.mp4", self.tmp)
            )
            video.download(output_path=output_path, filename=filename)
        if _type in {1, 3} and audio:
            (filename, output_path) = (
                (f"{self._title}_audio.mp3", self.app_path)
                if _type == 1
                else (f"{self.millis}.mp3", self.tmp)
            )
            audio.download(output_path=output_path, filename=filename)
        if video and audio and _type == 3:
            self._merge(v_out, a_out)
        print(f"Downloaded {self.watch_url}")

    def _merge(self, v_out: str, a_out: str):
        out_path = f"{self.app_path}\\{self._title}_{self.t_res}.mp4"
        if os.path.exists(out_path):
            raise _FileExistsError
        output = ffmpeg.output(
            ffmpeg.input(v_out),
            ffmpeg.input(a_out),
            out_path,
            vcodec="copy",
            acodec="copy",
            loglevel="quiet",
        )
        ffmpeg.run(output, overwrite_output=True, quiet=True)

x = PL(url="https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU")
x.download_video(3)


