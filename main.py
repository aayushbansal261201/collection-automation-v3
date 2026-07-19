from modules.summary import send_admin_summary
from modules.logger import logger
from modules.validator import validate_user_file
from modules.download_reports import download_reports
from modules.report_manager import ReportManager
from modules.filter_engine import filter_reports
from modules.email_service import send_emails

import time
import traceback


def main():

    start_time = time.time()

    logger.info("=" * 80)
    logger.info("COLLECTION AUTOMATION V3 STARTED")
    logger.info("=" * 80)

    try:

        # ==========================
        # STEP 1 : VALIDATE USERS
        # ==========================
        logger.info("STEP 1/5 : Validating Users")

        validate_user_file()

        logger.info("User validation completed successfully.")

        # ==========================
        # STEP 2 : DOWNLOAD REPORTS
        # ==========================
        logger.info("STEP 2/5 : Downloading Reports")

        from modules.cleanup import cleanup_temp

        logger.info("Cleaning old temporary files")

        cleanup_temp()

        logger.info("Downloading reports")

        download_reports()

        logger.info("Reports downloaded successfully.")

        # ==========================
        # STEP 3 : LOAD REPORTS INTO MEMORY
        # ==========================
        logger.info("STEP 3/5 : Loading Reports Into Memory")

        manager = ReportManager()

        reports = manager.load_reports()

        logger.info(f"{len(reports)} reports loaded into memory.")

        # ==========================
        # STEP 4 : FILTER REPORTS
        # ==========================
        logger.info("STEP 4/5 : Generating User Reports")

        filter_reports(reports)

        logger.info("Report generation completed successfully.")

        # ==========================
        # STEP 5 : SEND EMAILS
        # ==========================
    
        logger.info("STEP 5/5 : Sending Emails")

        summary_file, stats = send_emails()

        logger.info("All emails processed.")

        execution_time = round(time.time() - start_time, 2)

        if summary_file:
            send_admin_summary(
                summary_file=summary_file,
                stats=stats,
                execution_time=execution_time
            )
        else:
            logger.warning("Summary file not created. Admin email skipped.")

        logger.info("COLLECTION AUTOMATION COMPLETED SUCCESSFULLY")

    except Exception as e:

        logger.error("=" * 80)
        logger.error("AUTOMATION FAILED")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.error("=" * 80)

    finally:

        execution_time = round(time.time() - start_time, 2)

        logger.info("=" * 80)
        logger.info(f"Execution Time : {execution_time} Seconds")
        logger.info("COLLECTION AUTOMATION FINISHED")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()