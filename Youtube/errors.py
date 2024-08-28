# errors.py


class BaseCustomError(Exception):
    """Base class for custom exceptions with a default message."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DownloadError(BaseCustomError):
    """Exception raised for errors in downloading videos or playlists."""

    def __init__(
        self, message: str = "An error occurred while downloading the content"
    ):
        super().__init__(message)


class SaveError(BaseCustomError):
    """Exception raised for errors related to saving files."""

    def __init__(self, message: str = "An error occurred while saving the file"):
        super().__init__(message)


class MergeError(BaseCustomError):
    """Exception raised for errors in merging audio and video files."""

    def __init__(
        self, message: str = "An error occurred while merging audio and video"
    ):
        super().__init__(message)


class DirectoryError(BaseCustomError):
    """Exception raised for errors related to directory operations."""

    def __init__(self, message: str = "An error occurred with directory operations"):
        super().__init__(message)


class InvalidURLError(BaseCustomError):
    """Exception raised for errors related to invalid URLs."""

    def __init__(self, message: str = "The provided URL is invalid"):
        super().__init__(message)


class StreamSelectionError(BaseCustomError):
    """Exception raised for errors in selecting streams."""

    def __init__(self, message: str = "An error occurred while selecting streams"):
        super().__init__(message)


class DownloadTypeNotSupportedError(BaseCustomError):
    """Exception raised for unsupported download types."""

    def __init__(self, message: str = "The specified download type is not supported"):
        super().__init__(message)


class DirectoryCreationError(BaseCustomError):
    """Exception raised for errors in creating directories."""

    def __init__(self, message: str = "An error occurred while creating directories"):
        super().__init__(message)


class FFmpegError(BaseCustomError):
    """Exception raised for errors related to FFmpeg operations."""

    def __init__(self, message: str = "An error occurred while processing with FFmpeg"):
        super().__init__(message)


class PlaylistDownloadError(BaseCustomError):
    """Exception raised for errors in downloading playlists."""

    def __init__(
        self, message: str = "An error occurred while downloading the playlist"
    ):
        super().__init__(message)


class _FileExistsError(BaseCustomError):
    """Exception raised when a file already exists."""

    def __init__(self, message: str = "The file already exists"):
        super().__init__(message)


class TemporaryFileError(BaseCustomError):
    """Exception raised for errors related to temporary files."""

    def __init__(self, message: str = "An error occurred with temporary files"):
        super().__init__(message)


class DownloadAbortedError(BaseCustomError):
    """Exception raised when a download is aborted by the user."""

    def __init__(self, message: str = "The download has been aborted"):
        super().__init__(message)


class FailedDirectoryEmptyError(BaseCustomError):
    """Exception raised when emptying a directory fails."""

    def __init__(self, message: str = "The directory empty failed"):
        super().__init__(message)


class PlaylistExtractionError(BaseCustomError):
    """Exception raised when invalid URL/Playlist."""

    def __init__(self, message: str = "The playlist extraction failed"):
        super().__init__(message)
