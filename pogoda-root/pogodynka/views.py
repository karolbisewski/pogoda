from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import (
    TimeStamp,
    Prediction,
    PredictionType,
    PredicionTimeSpan,
    Location,
)

from django.conf import settings
import datetime, pytz
from django.utils import timezone
from django.utils.timezone import activate
from django.utils.translation import gettext as _
from django.utils.translation import get_language
activate(settings.TIME_ZONE)


def dates_view(request):
    qr = TimeStamp.objects.all().order_by('date')
    types = PredictionType.objects.all()

    context = {
        "page_title": _("History - Forecaster"),
        "prediction_types": types,
        "pre_checked_names": ['temperature', 'flux', 'wind_speed'],
        "object_list": qr,


    }
    return render(request, "dates.html", context)


def date_view(request, year, month, day, hour):
    time_zone = pytz.timezone(settings.TIME_ZONE)
    # https://stackoverflow.com/questions/20804837/weird-astimezone-behavior
    date_to_find_tz = time_zone.localize(datetime.datetime(year, month, day, hour))

    date_to_find_utc = date_to_find_tz.astimezone(pytz.utc)
    day_stamp = TimeStamp.objects.filter(date=date_to_find_utc).first()
    meteo_location = Location.objects.get(name='meteo')

    types = []
    for pred_type in get_list_or_404(PredictionType):
        spans = []
        for location in get_list_or_404(Location):
            preds = Prediction.objects.filter(type=pred_type, date=day_stamp, location=location).order_by('when')
            span = PredicionTimeSpan(pred_type, day_stamp, day_stamp, preds, location)
            spans.append(span)
        types.append(spans)
    # [
    #     [MeteoTempSpan, PolitechnikaTempSpan],
    #     [MeteoFluxSpan, PolitechnikaFluxSpan],
    #
    # ]
    context = {
        "page_title": _(f"Historia dla {day_stamp.get_slug} - Pogodynka"),
        'object': day_stamp,
        "location_span_list": types
    }
    return render(request, "date_detail.html", context)

# TODO: zabrać django time widgeta i podmienić go.