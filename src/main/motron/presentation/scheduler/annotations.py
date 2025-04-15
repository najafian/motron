import functools
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger  # Import DateTrigger
from datetime import datetime, timedelta

# Initialize the global scheduler
scheduler = BackgroundScheduler()

def Scheduled(cron=None, fixedDelay=None, initialDelay=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Mark this method as scheduled
        wrapper._is_scheduled = True

        # Prepare the trigger
        if cron:
            trigger = CronTrigger.from_crontab(cron)
            print(f"Scheduled task: {func.__name__} with cron expression {cron}")
        elif fixedDelay:
            trigger = IntervalTrigger(seconds=fixedDelay)
            print(f"Scheduled task: {func.__name__} with fixed delay of {fixedDelay} seconds")
        else:
            trigger = DateTrigger(run_date=datetime.now() + timedelta(seconds=initialDelay))
            print(f"Scheduled task: {func.__name__} with initial delay of {initialDelay} seconds")

        wrapper._scheduled_trigger = trigger
        return wrapper
    return decorator
