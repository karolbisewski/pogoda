from django.utils import timezone

from datetime import datetime
import traceback
import pytz
import time

def round_list(lst, places):
    "Rounds every float in lst. Precision decided by places"
    return list(map(lambda v: int(v * 10 ** places) / 10 ** places, lst))


def get_current_date_hour():
    t = timezone.now()
    d = datetime(t.year, t.month, t.day, t.hour, tzinfo=pytz.utc)
    return d


def nice_log_date(date):
    d = date

    y, m, d, h, mi = map(lambda x: str(x).zfill(2), [d.year, d.month, d.day, d.hour, d.minute])
    return f"{y}-{m}-{d} {h}:{mi}:00"


def every(delay, task):
    # execute task every _delay_ seconds
    next_time = time.time()
    while True:
        next_time += delay
        # next_time += (time.time() - next_time) // delay * delay + delay
        try:
            task()
        except Exception:
            traceback.print_exc()
        time.sleep(max(0, next_time - time.time()))
