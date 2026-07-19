

from dotenv import load_dotenv
import os

load_dotenv()

# ===============================
# EMAIL CONFIG
# ===============================

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"

# ===============================
# PATHS
# ===============================

USER_FILE = "data/users.xlsx"

REPORT_FOLDER = "reports"

OUTPUT_FOLDER = "output" 

TEMP_FOLDER = "temp"

LOG_FOLDER = "logs"

ARCHIVE_FOLDER = "archive"

FILTER_COLUMN = "Branch"

DOWNLOAD_TIMEOUT = 60

MAX_RETRIES = 3

# ===============================
# REPORTS
# ===============================

REPORTS = {
    "Payment Reconciliation": "http://172.235.29.24:9001/public/question/1c093dc3-8a95-4508-a157-18d71e4b2044.xlsx",
    "Exception Report": "http://172.235.29.24:9001/public/question/d16d3ab3-e778-485c-9328-8b3104b73ae2.xlsx",
    "Monthly LAN Activity": "http://172.235.29.24:9001/public/question/ab98d982-f732-45de-b621-6462fd45005c.xlsx",
    "Daily Activity": "http://172.235.29.24:9001/public/question/bb03c9db-00f1-4eeb-9203-e2e5ee520aa9.xlsx",
    "Receipt": "http://172.235.29.24:9001/public/question/ddfe0b02-18fb-4019-82e3-e88b936e6359.xlsx",
    "Lat-Long": "http://172.235.29.24:9001/public/question/f941da96-d887-4668-b55a-e2f8784d55a4.xlsx"
}
