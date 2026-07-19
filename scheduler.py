import schedule
import time

from main import main

schedule.every().day.at("09:00").do(main)
schedule.every().day.at("14:00").do(main)
schedule.every().day.at("18:00").do(main)

print("Scheduler Started...")

while True:
    schedule.run_pending()
    time.sleep(30)