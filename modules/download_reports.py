import os
import time
import requests

from config import REPORTS, REPORT_FOLDER, MAX_RETRIES, DOWNLOAD_TIMEOUT


def download_reports():

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    print("=" * 60)
    print("Downloading Reports...")
    print("=" * 60)

    for report_name, url in REPORTS.items():

        file_path = os.path.join(REPORT_FOLDER, f"{report_name}.xlsx")

        success = False

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                response = requests.get(url, timeout=DOWNLOAD_TIMEOUT)

                response.raise_for_status()

                with open(file_path, "wb") as f:
                    f.write(response.content)

                print(f"✓ {report_name} downloaded")

                success = True
                break

            except Exception as e:

                print(
                    f"Attempt {attempt} failed for {report_name}"
                )

                print(e)

                time.sleep(3)

        if not success:

            print(f"✗ Could not download {report_name}")

    print("\nDownload Completed.\n")


if __name__ == "__main__":
    download_reports()