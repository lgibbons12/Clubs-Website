from time import sleep
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from email_schedule.coolmain import send_email



def start():
    
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Set the CronTrigger to run every weekday (Monday to Friday) at 8 am
    trigger = CronTrigger(
        hour=8, minute=0, second=0, day_of_week='mon-fri'
    )
    scheduler.add_job(send_email, trigger=trigger)
    
    


if __name__ == "__main__":
    start()