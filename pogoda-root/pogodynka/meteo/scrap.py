import sys

sys.path.append('..')
sys.path.append('../..')

from . import mold
from datetime import datetime
from datetime import timedelta
from django.conf import settings
import pytz
from misc import (
    nice_log_date,
    get_current_date_hour,

)
from active import create_meteo_Prediction

# ----
def get_sample_times_for_next_week():
    sample_rate = 6  # one sample per 6 hours
    now = get_current_date_hour() - timedelta(days=5)
    hours_in_week = 7 * 24
    samples_in_week = hours_in_week // 6
    base_date = get_current_date_hour()
    base_date = datetime(base_date.year, base_date.month, base_date.day, tzinfo=pytz.UTC)
    date = base_date
    for _ in range(24 // sample_rate):  # there are this many samples per day
        for _ in range(7):  # per week
            yield date
            date = date + timedelta(hours=sample_rate)


# ----

def do_request(of_what: mold.RequestMold):
    for time, data in zip(*of_what.request()):
        # NOTE: maybe don't save older predictions that the prediciton itself is?
        create_meteo_Prediction(of_what.name, time, of_what.date, data)


def scrap(r_what, when):
    what = mold.mold_abstract_factory(r_what)(when)
    do_request(what)


def scrap_everything():
    for date in get_sample_times_for_next_week():
        for type in ["wind_speed", "wind_u", "wind_v", "flux", "temperature"]:
            try:
                scrap(type, date)
                print("Ok", type, date)
            except Exception as e:
                print(e)
                pass