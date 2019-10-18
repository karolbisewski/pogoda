import sys
import threading

sys.path.append("..")
sys.path.append("../..")

from pogodynka import setup

setup()

from django.conf import settings
from datetime import datetime, timedelta, time
from misc import get_current_date_hour, nice_log_date, every
import pytz
from time import sleep
from meteo import scrap
from politechnika import raspberry
# from machine.prepare import Data

def do_every_6_hours(func):
    def wrap(*args, **kwargs):
        every(60 * 60 * 6, lambda: log_wrapper(func, 6)(*args, **kwargs))

    return wrap


def do_every_1_hour(func):
    def wrap(*args, **kwargs):
        every(60 * 60 * 1, lambda: log_wrapper(func, 1)(*args, **kwargs))

    return wrap


def start_at_full_hour(func):
    def wrap(*args, **kwargs):
        to_sleep = 60 - datetime.now().minute - datetime.now().second / 60  # 60 is 1 hour
        print(f"Sleeping {func.__name__} for {to_sleep:.2f} minutes to start it at full hour.")
        # sleep(to_sleep)
        func(*args, **kwargs)

    return wrap


def log_wrapper(func, hours):
    def wrap(*args, **kwargs):
        print(f"{nice_log_date(datetime.now())}: Starting {func.__name__}...")
        # --
        func(*args, **kwargs)
        # --
        next_scrap_time_utc = get_current_date_hour() + timedelta(hours=hours)
        tz = pytz.timezone(settings.TIME_ZONE)
        next_scrap_time = next_scrap_time_utc.astimezone(tz)
        print(f"{nice_log_date(datetime.now().astimezone(tz))}: Next {func.__name__} start at {nice_log_date(next_scrap_time)}")

    return wrap


if __name__ == '__main__':
    DEBUG = ''

    if DEBUG:
        mode = DEBUG
    elif len(sys.argv) == 1:
        mode = 'both'
    elif len(sys.argv) == 2:
        _, mode = sys.argv
    else:
        print("Example usage:")
        print("python3.7 saver.py meteo")
        print("python3.7 saver.py politechnika")
        exit()

    mode = mode.lower()

    if mode in 'p politechnika local stacja lokalna both b'.split():
        threading.Thread(target=start_at_full_hour(do_every_1_hour(raspberry.save))).start()
    if mode in 'm meteo prognoza both b'.split():
        threading.Thread(target=start_at_full_hour(do_every_6_hours(scrap.scrap_everything))).start()
    if mode in 'l live podglad'.split():
        while True:
            raspberry.show()
