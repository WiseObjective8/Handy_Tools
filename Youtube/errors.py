class BaseCustomError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
class DownloadError(BaseCustomError):
    def __init__(
        self, message: str = "An error occurred while downloading the content"
    ):
        super().__init__(message)
class SaveError(BaseCustomError):
    def __init__(self, message: str = "An error occurred while saving the file"):
        super().__init__(message)
class MergeError(BaseCustomError):
    def __init__(
        self, message: str = "An error occurred while merging audio and video"
    ):
        super().__init__(message)
class DirectoryError(BaseCustomError):
    def __init__(self, message: str = "An error occurred with directory operations"):
        super().__init__(message)
class InvalidURLError(BaseCustomError):
    def __init__(self, message: str = "The provided URL is invalid"):
        super().__init__(message)
class StreamSelectionError(BaseCustomError):
    def __init__(self, message: str = "An error occurred while selecting streams"):
        super().__init__(message)
class DownloadTypeNotSupportedError(BaseCustomError):
    def __init__(self, message: str = "The specified download type is not supported"):
        super().__init__(message)
class DirectoryCreationError(BaseCustomError):
    def __init__(self, message: str = "An error occurred while creating directories"):
        super().__init__(message)
class FFmpegError(BaseCustomError):
    def __init__(self, message: str = "An error occurred while processing with FFmpeg"):
        super().__init__(message)
class PlaylistDownloadError(BaseCustomError):
    def __init__(
        self, message: str = "An error occurred while downloading the playlist"
    ):
        super().__init__(message)
class _FileExistsError(BaseCustomError):
    def __init__(self, message: str = "The file already exists"):
        super().__init__(message)
class TemporaryFileError(BaseCustomError):
    def __init__(self, message: str = "An error occurred with temporary files"):
        super().__init__(message)
class DownloadAbortedError(BaseCustomError):
    def __init__(self, message: str = "The download has been aborted"):
        super().__init__(message)
class FailedDirectoryEmptyError(BaseCustomError):
    def __init__(self, message: str = "The directory empty failed"):
        super().__init__(message)
class PlaylistExtractionError(BaseCustomError):
    def __init__(self, message: str = "The playlist extraction failed"):
        super().__init__(message)
