from main import setup
import sys
sys.path.append("..")
setup()

from pogodynka.models import (
    TimeStamp,
    Prediction,
    PredictionType,
    Location,
)
from django.conf import settings
import datetime
import pytz

speed_type = PredictionType.objects.get(name='wind_speed')
meteo_location = Location.objects.get(name='meteo')

# TODO move to utils or something
from_date = datetime.datetime(2019, 9, 1, tzinfo=pytz.utc)
to_date = datetime.datetime(2019, 9, 6, tzinfo=pytz.utc)

from_date = datetime.datetime.combine(from_date, datetime.time.min)
to_date = datetime.datetime.combine(to_date, datetime.time.max)

timezone = pytz.timezone(settings.TIME_ZONE)

from_date = timezone.localize(from_date)
to_date = timezone.localize(to_date)

hours = TimeStamp.objects.filter(date__range=(from_date, to_date)).order_by('date')

preds = []
for hour in hours:
    prediction = Prediction.objects.filter(type=speed_type, location=meteo_location, date=hour).order_by('-when').first()
    x = (prediction.date, prediction.value)
    preds.append(x)
