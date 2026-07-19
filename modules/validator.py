import os
import pandas as pd

from config import USER_FILE
from modules.logger import logger


def validate_user_file():
    """
    Validate users.xlsx before automation starts.
    """

    if not os.path.exists(USER_FILE):
        raise FileNotFoundError(f"{USER_FILE} not found.")

    users = pd.read_excel(USER_FILE)

    required_columns = [
        "User_name",
        "Email",
        "Area_under_him"
    ]

    for col in required_columns:
        if col not in users.columns:
            raise Exception(f"Missing required column: {col}")

    if users.empty:
        raise Exception("users.xlsx is empty.")

    logger.info(f"User validation successful. Total Users: {len(users)}")

    return users