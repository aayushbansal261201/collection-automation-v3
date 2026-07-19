

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
    "Payment Reconciliation": "dummy1.xlsx",
    "Exception Report": "dummy2.xlsx",
    "Monthly LAN Activity": "http://172.235.29.24:9001/public/question/ab98.xlsx",
    "Daily Activity": "http://172.235.29.24:9001/public/question/bb03c9db-00f1-4eeb-9.xlsx",
    "Receipt": "http://172.235.29.24:9001/public/question/ddfe0b02-18fb-4019-82e3-e.xlsx",
    "Lat-Long": "http://172.235.29.24:9001/public/question/f941da96-d887-4668-b55a-e.xlsx"
}
