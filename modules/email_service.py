import os
import time
import shutil
import smtplib
import mimetypes
import pandas as pd

from email.message import EmailMessage
from email.utils import formatdate
from datetime import datetime

from config import (
    USER_FILE,
    TEMP_FOLDER,
    EMAIL,
    PASSWORD,
    SMTP_SERVER,
    SMTP_PORT
)

from modules.logger import logger
from modules.summary import Summary


summary = Summary()


def create_html_email(user_name, report_count):

    today = datetime.now().strftime("%d-%b-%Y %I:%M %p")

    return f"""
<html>

<head>

<style>

body {{
    font-family: Arial;
    color:#333;
}}

table {{

border-collapse: collapse;

}}

td,th {{

padding:8px;

border:1px solid #ddd;

}}

</style>

</head>

<body>

<h2>Collection MIS Reports</h2>

<p>

Hello <b>{user_name}</b>,

</p>

<p>

Please find attached today's Collection MIS Reports.

</p>

<table>

<tr>

<th>Date</th>

<td>{today}</td>

</tr>

<tr>

<th>Total Reports</th>

<td>{report_count}</td>

</tr>

</table>

<br>

<p>

This email is automatically generated.

</p>

<br>

Regards,

<br>

<b>IT Team</b>

</body>

</html>
"""


def send_emails():

    logger.info("=" * 70)
    logger.info("EMAIL SERVICE STARTED")
    logger.info("=" * 70)

    users = pd.read_excel(USER_FILE)

    sent = 0
    failed = 0
    skipped = 0

    try:

        server = smtplib.SMTP_SSL(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=60
        )

        server.login(
            EMAIL,
            PASSWORD
        )

        logger.info("SMTP Login Successful")

    except Exception as e:

        logger.error(f"SMTP Login Failed : {e}")

        return None, {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0
    }

    total_users = len(users)

    logger.info(f"Total Users : {total_users}")

    for _, user in users.iterrows():
        
        name = str(user["User_name"]).strip()
        receiver = str(user["Email"]).strip()

        logger.info("-" * 60)
        logger.info(f"Processing : {name}")

        # ------------------------------
        # Validate Email
        # ------------------------------

        if (
            receiver == ""
            or receiver.lower() == "nan"
            or "@" not in receiver
        ):

            logger.warning(
                f"{name} : Invalid Email Address"
            )

            skipped += 1

            summary.add(
                user=name,
                email=receiver,
                status="SKIPPED",
                reports=0,
                remarks="Invalid Email"
            )

            continue

        folder = os.path.join(
            TEMP_FOLDER,
            name
        )

        if not os.path.exists(folder):

            logger.warning(
                f"{name} : Folder Not Found"
            )

            skipped += 1

            summary.add(
                user=name,
                email=receiver,
                status="SKIPPED",
                reports=0,
                remarks="Folder Not Found"
            )

            continue

        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.endswith(".xlsx")
        ]

        if len(files) == 0:

            logger.warning(
                f"{name} : No Reports Generated"
            )

            skipped += 1

            summary.add(
                user=name,
                email=receiver,
                status="SKIPPED",
                reports=0,
                remarks="No Reports"
            )

            continue

        # ------------------------------
        # Attachment Size Check
        # ------------------------------

        total_size = sum(
            os.path.getsize(file)
            for file in files
        )

        logger.info(
            f"{name} : {len(files)} Reports | "
            f"{round(total_size/1024/1024,2)} MB"
        )

        msg = EmailMessage()

        msg["Subject"] = (
            f"Collection MIS Reports - "
            f"{datetime.now().strftime('%d-%b-%Y')}"
        )

        msg["From"] = EMAIL

        msg["To"] = receiver

        msg["Date"] = formatdate(localtime=True)

        msg.set_content(
            "Please view this email in HTML."
        )

        msg.add_alternative(
            create_html_email(
                name,
                len(files)
            ),
            subtype="html"
        )

        # ------------------------------
        # Attach Reports
        # ------------------------------

        for file in files:

            mime_type, _ = mimetypes.guess_type(file)

            if mime_type is None:

                mime_type = "application/octet-stream"

            maintype, subtype = mime_type.split("/")

            with open(file, "rb") as attachment:

                msg.add_attachment(
                    attachment.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(file)
                )

        # ------------------------------
        # Retry Logic
        # ------------------------------

        success = False

        for attempt in range(3):

            try:

                server.send_message(msg)

                logger.info(
                    f"{name} : Email Sent"
                )

                sent += 1

                success = True

                break

            except Exception as e:

                logger.error(
                    f"{name} : Attempt {attempt+1} Failed : {e}"
                )

                time.sleep(2)

                try:

                    server.quit()

                except:
                    pass

                try:

                    server = smtplib.SMTP_SSL(
                        SMTP_SERVER,
                        SMTP_PORT,
                        timeout=60
                    )

                    server.login(
                        EMAIL,
                        PASSWORD
                    )

                except Exception as smtp_error:

                    logger.error(
                        smtp_error
                    )

        # ------------------------------
        # SUCCESS
        # ------------------------------

        if success:

            summary.add(
                user=name,
                email=receiver,
                status="SUCCESS",
                reports=len(files),
                remarks=""
            )

            try:

                shutil.rmtree(folder)

                logger.info(
                    f"{name} : Temporary Folder Deleted"
                )

            except Exception as e:

                logger.error(
                    f"{name} : Folder Delete Failed : {e}"
                )

        # ------------------------------
        # FAILED
        # ------------------------------

        else:

            failed += 1

            summary.add(
                user=name,
                email=receiver,
                status="FAILED",
                reports=len(files),
                remarks="SMTP Failed"
            )

    # --------------------------------------
    # CLOSE SMTP
    # --------------------------------------

    try:

        server.quit()

        logger.info("SMTP Connection Closed")

    except Exception:

        pass

    # --------------------------------------
    # SAVE SUMMARY
    # --------------------------------------

    try:

        summary_file = summary.save()

        stats = summary.statistics()

        logger.info(f"Summary File : {summary_file}")

    except Exception as e:

        logger.error(f"Summary Error : {e}")

        summary_file = None

        stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0
        }

    # --------------------------------------
    # FINAL LOG
    # --------------------------------------

    logger.info("=" * 70)

    logger.info("EMAIL SERVICE COMPLETED")

    logger.info(f"Emails Sent     : {sent}")

    logger.info(f"Emails Failed   : {failed}")

    logger.info(f"Users Skipped   : {skipped}")

    logger.info("=" * 70)

    return summary_file, stats


if __name__ == "__main__":

    send_emails()

    