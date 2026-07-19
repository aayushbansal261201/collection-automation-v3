import os
import pandas as pd

from config import REPORT_FOLDER, REPORTS
from modules.logger import logger


class ReportManager:

    def __init__(self):
        self.reports = {}

    def load_reports(self):

        logger.info("=" * 60)
        logger.info("LOADING REPORTS INTO MEMORY")
        logger.info("=" * 60)

        self.reports.clear()

        for report_name in REPORTS.keys():

            file_path = os.path.join(
                REPORT_FOLDER,
                f"{report_name}.xlsx"
            )

            if not os.path.exists(file_path):

                logger.warning(
                    f"{report_name} not found."
                )

                continue

            try:

                df = pd.read_excel(
                    file_path,
                    engine="openpyxl"
                )

                logger.info(
                    f"{report_name} : {len(df)} rows"
                )

                self.reports[report_name] = df

            except Exception as e:

                logger.error(
                    f"{report_name} : {e}"
                )

        logger.info(
            f"Loaded {len(self.reports)} reports."
        )

        return self.reports

    def get_report(self, report_name):

        return self.reports.get(report_name)