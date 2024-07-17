import argparse
import logging
from pytubefix import YouTube
from typing import Callable, Any, Dict, Optional
import os
import time
import shutil
import ffmpeg
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download_log.log'),
        logging.StreamHandler()
    ]
)


class Download(YouTube):

    def __init__(self, url: str, client: str = 'ANDROID_TESTSUITE',
                 on_progress_callback: Optional[Callable[[
                     Any, bytes, int], None]] = None,
                 on_complete_callback: Optional[Callable[[
                     Any, Optional[str]], None]] = None,
                 proxies: Optional[Dict[str, str]] = None, use_oauth: bool = False,
                 allow_oauth_cache: bool = True):
        super().__init__(url, client, on_progress_callback,
                         on_complete_callback, proxies, use_oauth, allow_oauth_cache)
        self.uprof = os.path.expanduser("~")
        try:
            os.makedirs(os.path.join(self.uprof, "Downloads",
                        "YT", "tmp"), exist_ok=True)
        except OSError as e:
            logging.error(f"Failed to create directories: {e}")
            raise
        self.destination = os.path.join(self.uprof, "Downloads", "YT")
        self.tmp = os.path.join(self.uprof, "Downloads", "YT", "tmp")
        self.millis = int(time.time() * 1000)

    def empty_folder(self, folder_path):
        if not os.path.exists(folder_path):
            logging.warning(f"The folder {folder_path} does not exist.")
            return
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")

    def download_video(self, download_type: int = 3, resolution: int = 1):
        dty = {
            1: 'audio',
            2: 'video',
            3: 'both'
        }
        res = {
            1: '1080p',
            2: '720p',
            3: '480p'
        }
        try:
            audio = self.streams.get_audio_only()
            video = self.streams.filter(
                res=res[resolution]).first() if resolution else None

            v_out = os.path.join(self.tmp, f'{self.millis}.mp4')
            a_out = os.path.join(self.tmp, f'{self.millis}.mp3')

            if download_type > 1 and video:
                if download_type == 2:
                    video.download(output_path=self.destination,
                                   filename=f"{self.title}.mp4")
                elif not os.path.exists(v_out):
                    v_out = video.download(
                        output_path=self.tmp, filename=f"{self.millis}.mp4")

            if download_type % 2 != 0 and audio:
                if download_type == 1:
                    audio.download(output_path=self.destination,
                                   filename=f"{self.title}.mp3")
                elif not os.path.exists(a_out):
                    a_out = audio.download(
                        output_path=self.tmp, filename=f"{self.millis}.mp3")

            if video and audio and download_type == 3:
                out = os.path.join(self.destination, f"{self.title}.mp4")
                if os.path.exists(out):
                    raise Exception("Another file with same name exists")
                v_in = ffmpeg.input(str(v_out))
                a_in = ffmpeg.input(str(a_out))
                o_out = ffmpeg.output(
                    v_in, a_in, out, vcodec='copy', acodec='copy')
                ffmpeg.run(o_out, overwrite_output=True)

            logging.info(f"Download completed for {self.watch_url}")
            print(f"Download is completed successfully for {self.title}")
        except ValueError as ve:
            logging.error(f"Stream selection error: {ve}")
            print(f"Stream selection error for {self.title}: {ve}")
        except Exception as e:
            logging.error(f"An error occurred with {self.watch_url}: {str(e)}")
            print(f"An error has occurred with {self.title}")
            print(e)
        finally:
            self.empty_folder(self.tmp)
            print(f"All videos are saved at: {self.destination}")


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Downloader")
    parser.add_argument("--link", nargs='+', help="YouTube video link(s)")

    args = parser.parse_args()
    dty = {
        1: 'audio',
        2: 'video',
        3: 'both'
    }
    res = {
        1: '1080p',
        2: '720p',
        3: '480p'
    }
    def helper(link):
        download_type = input("Choose download type\n1. audio\n2. video\n3. both\nLeave blank for [3]: ").strip().lower() or 3
        resolution = input("Choose resolution\n1. 1080p\n2. 720p\n3. 480p\nLeave blank for [1]: ").strip().lower() or 1 if download_type > 1 else None
        confirmation = input(f"Proceed with downloading {dty[download_type]} in {res[resolution]}? (yes/no)\nLeave blank for [yes]: ").strip().lower() or 'yes' if download_type in [2, 3] else input(f"Proceed with downloading {dty[download_type]}? (yes/no)\nLeaver blank for [yes]: ").strip().lower()
        if confirmation != 'no':
            try:
                Download(link).download_video(download_type, resolution)
            except Exception as e:
                logging.error(f"Failed to download {link}: {e}")
        else:
            print("Download aborted.")
    if not args.link:
        link = input("Enter video URL: ").strip()
        helper(link)
    else:
        for link in args.link:
                helper(link)

if __name__ == "__main__":
    main()
