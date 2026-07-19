import os
import shutil

from config import TEMP_FOLDER
from modules.logger import logger


def cleanup_temp():

    logger.info("=" * 60)
    logger.info("CLEANING TEMP DIRECTORY")
    logger.info("=" * 60)

    if not os.path.exists(TEMP_FOLDER):

        logger.info("Temp folder does not exist.")

        return

    deleted = 0

    for item in os.listdir(TEMP_FOLDER):

        path = os.path.join(
            TEMP_FOLDER,
            item
        )

        try:

            if os.path.isdir(path):

                shutil.rmtree(path)

                deleted += 1

            else:

                os.remove(path)

                deleted += 1

        except Exception as e:

            logger.error(
                f"Unable to delete {item} : {e}"
            )

    logger.info(
        f"Deleted {deleted} old folders/files."
    )

    logger.info("=" * 60)