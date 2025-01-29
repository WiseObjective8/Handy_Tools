import logging
import os
from Youtube.errors import BaseCustomError
from datetime import datetime

LOG_DIR = os.path.join(
    os.path.expanduser("~"), "Documents", "Github", "Handy_tools", "Youtube", "logs"
)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(
    LOG_DIR, f"youtube_downloader_{datetime.now().strftime('%Y%m%d')}.log"
)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # Append mode
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("Youtube")
logger_gui = logging.getLogger("YT-GUI")
logger_pytube = logging.getLogger("pytubefix").setLevel(logging.WARNING)
logger.propagate = False
logger_gui.propagate = False


def log_exception(exc: BaseCustomError):
    """Log exceptions using the logger."""
    logger.error(f"{exc.__class__.__name__}: {exc.message}")
