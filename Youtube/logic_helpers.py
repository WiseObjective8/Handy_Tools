'''Hepler methods for yt_vid and yt_playlist'''
import os
import re
from Youtube.logs import log_setup, logging

log_setup()


APP_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "YoutubeDownloader")


def handle_errors(custom_exception):
    """
    A decorator for handling exceptions in functions.

    This decorator wraps a function and catches any exceptions that occur during its execution. 
    If an exception is raised, it logs the error and raises a specified custom exception.

    Args:
        custom_exception (Exception): The custom exception to raise when an error occurs.

    Returns:
        function: The wrapped function that includes error handling.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(e)
                raise custom_exception from e

        return wrapper

    return decorator


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename by removing invalid characters.

    This function takes a filename as input and removes any characters that are invalid in file names. 
    It ensures that the resulting filename is safe for use in file operations.

    Args:
        filename (str): The original filename to sanitize.

    Returns:
        str: The sanitized filename with invalid characters removed.
"""

    invalid_chars_pattern = r'[\\\/:*?"<>|]'
    return re.sub(invalid_chars_pattern, "", filename)
