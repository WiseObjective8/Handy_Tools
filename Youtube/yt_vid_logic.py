"""
A class that extends the YouTube functionality for downloading videos.
Args:
    url (str): The URL of the YouTube video to download.
    client (str, optional): The client _type for the download. Defaults to "ANDROID_TESTSUITE".
    on_progress_callback (Callable[[Any, bytes, int], None] | None, optional):
        A callback function that is called during the download process.
    on_complete_callback (Callable[[Any, str | None], None] | None, optional):
        A callback function that is called when the download is complete.
    proxies (Dict[str, str] | None, optional): A dictionary of proxy settings to use for the connection.
    use_oauth (bool, optional): Whether to use OAuth for authentication. Defaults to False.
    allow_oauth_cache (bool, optional): Whether to allow caching of OAuth tokens. Defaults to True.
    token_file (str | None, optional): The file path to store the OAuth token.
Returns:
    None
"""
# pylint: disable = line-too-long
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
from Youtube.logs import log_setup, logging
from Youtube.logic_helpers import APP_PATH, handle_errors, sanitize_filename

log_setup()
class YT(YouTube):
    """Youtube Class"""

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
        use_oauth: bool = False,
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
        self.regex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        if not re.match(self.regex, self.url):
            raise InvalidURLError
        self._type = {1: "audio", 2: "video", 3: "both"}
        self.res = {1: "1080p", 2: "720p", 3: "480p"}
        self.t_res = ""
        self.app_path = app_path
        self._title = sanitize_filename(self.title)
        self.tmp = os.path.join(self.app_path, "tmp")
        self._create_directories()

    @handle_errors(DirectoryCreationError)
    def _create_directories(self):
        """
        Create necessary directories for storing downloads if they do not exist.
        """
        if not os.path.exists(self.app_path):
            os.makedirs(self.app_path, exist_ok=True)
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp, exist_ok=True)

    @handle_errors(DownloadError)
    def download_video(self, _type: int, resolution: int = None):
        """
        Start the download process based on the specified _type and resolution.

        :param _type: Type of download (1: audio, 2: video, 3: both).
        :param resolution: Resolution of the video to download (1: 1080p, 2: 720p, 3: 480p).
        """
        self._extract_streams(_type, resolution)
        self.empty_folder(self.tmp)  # Clean up temporary files after processing

    @handle_errors(FailedDirectoryEmptyError)
    def empty_folder(self, path: str) -> None:
        """
        Remove all files and subdirectories in the specified folder.

        :param path: Path to the folder to be emptied.
        """
        if os.path.exists(path):
            shutil.rmtree(path)  # Remove the folder and its contents

    @handle_errors(InvalidURLError)
    def _extract_streams(self, _type: int, resolution: int = None):
        """
        Extract the video and audio streams based on the download _type and resolution.

        :param _type: Type of download (1: audio, 2: video, 3: both).
        :param resolution: Resolution of the video to download (1: 1080p, 2: 720p, 3: 480p).
        """
        self.t_res = self.res[resolution] if resolution else "1080p"
        audio = (
            self.streams.get_audio_only() if _type in {1, 3} else None
        )  # Get audio stream
        video = (
            self.streams.filter(res=self.t_res).first() if resolution else None
        )  # Get video stream with specified resolution
        if _type == 1:
            audio = self.streams.get_audio_only()  # Get audio stream
            video = None
        elif _type == 2:
            audio = None
            video = (
                self.streams.filter(res=self.t_res).first() if resolution else None
            )  # Get video stream with specified resolution
        elif _type == 3:
            audio = self.streams.get_audio_only()  # Get audio stream
            video = self.streams.filter(res=self.t_res).first() if resolution else None
        self._processdata(_type, video, audio)

    @handle_errors(DownloadError)
    def _processdata(self, _type: int, video: Stream = None, audio: Stream = None):
        """
        Download and process video and audio streams according to the specified _type.

        :param _type: Type of download (1: audio, 2: video, 3: both).
        :param video: Video stream object.
        :param audio: Audio stream object.
        """
        # pylint: disable = attribute-defined-outside-init
        self.millis = int(time.time() * 1000)  # Current timestamp in milliseconds
        # Generate output paths with timestamp
        v_out = os.path.join(self.tmp, f"{self.millis}.mp4")
        a_out = os.path.join(self.tmp, f"{self.millis}.mp3")

        # Download video if required
        if _type in {2, 3} and video:
            (filename, output_path) = (
                (f"{self._title}_{self.t_res}_video.mp4", self.app_path)
                if _type == 2
                else (f"{self.millis}.mp4", self.tmp)
            )
            video.download(output_path=output_path, filename=filename)

        # Download audio if required
        if _type in {1, 3} and audio:
            (filename, output_path) = (
                (f"{self._title}_audio.mp3", self.app_path)
                if _type == 1
                else (f"{self.millis}.mp3", self.tmp)
            )
            audio.download(output_path=output_path, filename=filename)

        # Merge video and audio if both are downloaded
        if video and audio and _type == 3:
            self._merge(v_out, a_out)

        # Log and print the completion status
        logging.info(f"Downloaded {self.watch_url}")
#        print(f"Downloaded {self._title}")

    @handle_errors(FFmpegError)
    def _merge(self, v_out: str, a_out: str):
        """
        Merge the video and audio files into a single output file.

        :param v_out: Path to the video file.
        :param a_out: Path to the audio file.
        """
        out_path = (
            f"{self.app_path}\\{self._title}_{self.t_res}.mp4"  # Output file path
        )
        if os.path.exists(out_path):
            raise _FileExistsError  # Ensure the output file does not already exist
        # Merge video and audio using FFmpeg
        output = ffmpeg.output(
            ffmpeg.input(v_out),
            ffmpeg.input(a_out),
            out_path,
            vcodec="copy",
            acodec="copy",
            loglevel="quiet"
        )
        ffmpeg.run(output, overwrite_output=True)
