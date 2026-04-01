import threading
import schedule
import time
from datetime import datetime
import pytz
from logger import logger
from scheduler import run_daily_task
from telegram_bot import run_bot

def scheduler_thread():
    def job():
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
        if now.hour == 9 and now.minute == 0:
            logger.info("Running scheduled job...")
            run_daily_task()

    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Start scheduler in background
    sched_thread = threading.Thread(target=scheduler_thread, daemon=True)
    sched_thread.start()

    # Start Telegram bot (blocking, runs in main thread)
    logger.info("Starting Telegram bot...")
    run_bot()
