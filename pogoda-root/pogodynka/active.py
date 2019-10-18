import sys

# TODO: ADD WIND DIRECTION TO GRAPH
# TODO: ADD PREDICTIONS TO GRAPH

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../pogoda")

from pogoda import main

main.setup()
from django.conf import settings

from datetime import datetime, timedelta
import pytz

from pogodynka.models import (
    TimeStamp,
    Prediction,
    PredictionType,
    Location,
)

meteo_location = Location.objects.get(name='meteo')
politechnika_location = Location.objects.get(name='politechnika')
model_prediction_location = Location.objects.get(name='politechnika')


def create_meteo_Prediction(type, time, when, value):
    create_Prediction(type, time, when, value, meteo_location)


def create_politechnika_Prediction(type, time, value):
    create_Prediction(type, time, time, value, politechnika_location)


def create_model_Prediction(type, time, value):
    create_Prediction(type, time, time, value, model_prediction_location)


def create_TimeStamp(date):
    results = TimeStamp.objects.filter(date=date)
    if results.count() == 0:
        new = TimeStamp(date=date)
        new.save()
        return new
    else:
        return results.first()


def create_Prediction(type_name, time, when, value, location):
    print(".", end='')
    stamp = create_TimeStamp(time)
    type = get_PredictionType(type_name)
    num_results = Prediction.objects.filter(type=type, when=when, date=stamp)
    if num_results.count() == 0:
        new = Prediction(type=type, when=when, date=stamp, value=value, location=location)
        new.save()
    else:
        # print('Prediction already exists.')
        pass


def get_PredictionType(name):
    type = PredictionType.objects.filter(name=name).first()
    if not type:
        rec = input(
            f'There is no such PredictionType of name = {name} in Database.\nDo you want to create new one? (Y/N): ')
        if rec.strip().lower() in ('y', 'yes', 't', 'tak'):
            type = PredictionType(name=name)
            type.save()
        else:
            raise ValueError(f"There is no such PredictionType of name = {name} in Database. Maybe you misstyped?")
    return type


def get_politechnika_24_Predictions(date, type):
    preds = get_x_Predictions(type, politechnika_location, date, 1)
    assert len(preds) == 24
    return preds


def get_meteo_48_Predictions(date, type):
    preds = get_x_Predictions(type, meteo_location, date, 2)
    assert len(preds) == 48
    return preds


def get_x_Predictions(type, location, from_date, x_days):
    to_date = from_date + timedelta(days=x_days)

    from_date = datetime.combine(from_date, datetime.time.min)
    to_date = datetime.combine(to_date, datetime.time.max)

    timezone = pytz.timezone(settings.TIME_ZONE)

    from_date = timezone.localize(from_date)
    to_date = timezone.localize(to_date)

    hours = TimeStamp.objects.filter(date__range=(from_date, to_date)).order_by('date')

    type = get_PredictionType(type)

    preds = []
    for hour in hours:
        prediction = Prediction.objects.filter(type=type, location=location,
                                               date=hour).order_by('-when').first()
        preds.append(prediction.value)

    return preds
