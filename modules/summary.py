import smtplib
import mimetypes

from email.message import EmailMessage

from config import (
    EMAIL,
    PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    ADMIN_EMAIL
)
import os
from datetime import datetime
import pandas as pd

from modules.logger import logger
from config import LOG_FOLDER


class Summary:

    def __init__(self):
        self.records = []

    def add(
        self,
        user,
        email,
        status,
        reports,
        remarks=""
    ):

        self.records.append(
            {
                "User": user,
                "Email": email,
                "Status": status,
                "Reports": reports,
                "Remarks": remarks,
                "Time": datetime.now().strftime("%H:%M:%S")
            }
        )

    def save(self):

        if len(self.records) == 0:
            logger.warning("No summary data found.")
            return None

        today = datetime.now().strftime("%Y-%m-%d")

        folder = os.path.join(
            LOG_FOLDER,
            today
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        file = os.path.join(
            folder,
            "email_summary.xlsx"
        )

        pd.DataFrame(
            self.records
        ).to_excel(
            file,
            index=False
        )

        logger.info(
            f"Summary Saved : {file}"
        )

        return file

    def statistics(self):

        total = len(self.records)

        sent = len(
            [
                x
                for x in self.records
                if x["Status"] == "SUCCESS"
            ]
        )

        failed = len(
            [
                x
                for x in self.records
                if x["Status"] == "FAILED"
            ]
        )

        skipped = len(
            [
                x
                for x in self.records
                if x["Status"] == "SKIPPED"
            ]
        )

        logger.info("=" * 60)
        logger.info(f"Total Users : {total}")
        logger.info(f"Success    : {sent}")
        logger.info(f"Failed     : {failed}")
        logger.info(f"Skipped    : {skipped}")
        logger.info("=" * 60)

        return {
            "total": total,
            "success": sent,
            "failed": failed,
            "skipped": skipped
        }
    
def send_admin_summary(summary_file, stats, execution_time):

    try:

        msg = EmailMessage()

        msg["Subject"] = (
            "Collection Automation Summary - "
            + datetime.now().strftime("%d-%b-%Y")
        )

        msg["From"] = EMAIL

        msg["To"] = ADMIN_EMAIL

        msg.set_content(f"""
Collection Automation Completed Successfully

Execution Time : {execution_time} Seconds

Total Users : {stats['total']}

Emails Sent : {stats['success']}

Emails Failed : {stats['failed']}

Users Skipped : {stats['skipped']}

Regards,

Collection Automation
""")

        if summary_file and os.path.exists(summary_file):

            mime_type, _ = mimetypes.guess_type(summary_file)

            if mime_type is None:
                mime_type = "application/octet-stream"

            maintype, subtype = mime_type.split("/")

            with open(summary_file, "rb") as f:

                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(summary_file)
                )

        server = smtplib.SMTP_SSL(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.login(
            EMAIL,
            PASSWORD
        )

        server.send_message(msg)

        server.quit()

        logger.info("Admin Summary Email Sent")

    except Exception as e:

        logger.error(f"Admin Summary Failed : {e}")