"""Hepler methods for yt_vid and yt_playlist"""

import os
import re
from Youtube.logs import log_exception
from Youtube.errors import InvalidURLError

APP_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "YoutubeDownloader")


def handle_errors(custom_exception):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_exception(e)
                raise custom_exception from e

        return wrapper

    return decorator


def sanitize_filename(filename: str) -> str:
    invalid_chars_pattern = r'[\\\/:*?"<>|]'
    return re.sub(invalid_chars_pattern, "", filename)

def url_check(url: str) -> int:
    vid_regex = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")
    playlist_regex = re.compile(r"(?:http|https|)(?::\/\/|)(?:www.|)(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/ytscreeningroom\?v=|\/feeds\/api\/videos\/|\/user\S*[^\w\-\s]|\S*[^\w\-\s]))([\w\-]{12,})[a-z0-9;:@#?&%=+\/\$_.-]*")
    try:
        if re.match(playlist_regex, url):
            return 1
        elif re.match(vid_regex, url):
            return 0
        else:
            raise InvalidURLError(f"{url} is invalid")
    except Exception as e:
        log_exception(e)
