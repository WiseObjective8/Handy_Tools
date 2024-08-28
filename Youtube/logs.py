# pylint: disable = missing-function-docstring
# pylint: disable = missing-module-docstring
import logging
def log_setup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        handlers=[logging.FileHandler("download_log.txt")],
    )
