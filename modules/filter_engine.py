import os
import warnings
import pandas as pd

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="openpyxl"
)

from config import (
    REPORTS,
    TEMP_FOLDER,
    USER_FILE,
    FILTER_COLUMN
)

from modules.logger import logger


def clean_text(value):

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def get_user_branches(branch_string):

    if pd.isna(branch_string):
        return []

    return [
        clean_text(x)
        for x in str(branch_string).split(",")
        if x.strip()
    ]


def filter_reports(reports):

    logger.info("=" * 70)
    logger.info("GENERATING USER REPORTS")
    logger.info("=" * 70)

    users = pd.read_excel(USER_FILE)

    os.makedirs(TEMP_FOLDER, exist_ok=True)

    total_users = len(users)

    logger.info(f"Total Users : {total_users}")

    total_reports = 0

    for index, user in users.iterrows():

        user_name = str(user["User_name"]).strip()

        logger.info(
            f"[{index+1}/{total_users}] Processing : {user_name}"
        )

        branches = get_user_branches(
            user["Area_under_him"]
        )

        if len(branches) == 0:

            logger.warning(
                f"{user_name} : No Branch Assigned"
            )

            continue

        user_folder = os.path.join(
            TEMP_FOLDER,
            user_name
        )

        os.makedirs(
            user_folder,
            exist_ok=True
        )

        for report_name, df in reports.items():

            try:

                if FILTER_COLUMN not in df.columns:

                    logger.warning(
                        f"{report_name} : '{FILTER_COLUMN}' column missing"
                    )

                    continue

                working_df = df.copy()

                working_df["_filter"] = (
                    working_df[FILTER_COLUMN]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                filtered = working_df[
                    working_df["_filter"].isin(branches)
                ].copy()

                filtered.drop(
                    columns="_filter",
                    inplace=True
                )

                if filtered.empty:

                    continue

                output_file = os.path.join(
                    user_folder,
                    f"{report_name}.xlsx"
                )

                with pd.ExcelWriter(
                    output_file,
                    engine="xlsxwriter"
                ) as writer:

                    filtered.to_excel(
                        writer,
                        index=False,
                        sheet_name="Report"
                    )

                total_reports += 1

                logger.info(
                    f"{user_name} -> {report_name} ({len(filtered)} rows)"
                )

            except Exception as e:

                logger.error(
                    f"{user_name} | {report_name} : {e}"
                )

    logger.info("=" * 70)
    logger.info("REPORT GENERATION COMPLETED")
    logger.info(f"Users Processed : {total_users}")
    logger.info(f"Reports Created : {total_reports}")
    logger.info("=" * 70)