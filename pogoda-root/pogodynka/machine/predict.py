from active import create_model_Prediction, get_politechnika_24_Predictions, get_meteo_48_Predictions
from misc import get_current_date_hour
from datetime import datetime, timedelta
from . import model
import pytz
import sys

sys.path.append('..')
sys.path.append('../..')
from django.conf import settings


def save():
    start_date = get_current_date_hour()
    for prediction_name in ['flux', 'wind_speed']:
        predicitons = model.get_24h_predictions(get_politechnika_24_Predictions(start_date, prediction_name),
                                                get_meteo_48_Predictions(start_date, prediction_name),
                                                prediction_name)
        for_when = start_date
        for value in predicitons:
            create_model_Prediction(prediction_name,
                                    for_when,
                                    value)
            for_when = for_when + timedelta(hours=1)
