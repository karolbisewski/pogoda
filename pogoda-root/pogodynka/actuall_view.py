from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.conf import settings

import datetime
import pytz

from .models import (
    TimeStamp,
    Prediction,
    PredictionType,
    PredicionTimeSpan,
    Location,
)
from django.utils.translation import gettext as _


def get_future_spans(year, month, day, hour, of_what):
    "Returns list of PredicionTimeSpans"
    if isinstance(of_what, str):
        of_what = of_what.split(",")
        if isinstance(of_what, str):
            of_what = [of_what]

    from_date = datetime.datetime(year, month, day, tzinfo=pytz.utc)
    from_date = datetime.datetime.combine(from_date, datetime.time(hour=hour))
    to_date = datetime.datetime.combine(from_date, datetime.time.max) + datetime.timedelta(hours=hour)

    timezone = pytz.timezone(settings.TIME_ZONE)

    from_date = timezone.localize(from_date)
    to_date = timezone.localize(to_date)

    date_stamps = TimeStamp.objects.filter(date__range=(from_date, to_date)).order_by('date')
    locations_span_list = {}

    types = []
    for type_name in of_what:
        spans_list = []
        for location in get_list_or_404(Location)[::-1]:
            type = get_object_or_404(PredictionType, name=type_name)

            bests = []
            for date_stamp in date_stamps:

                best_prediction = Prediction.objects.filter(type=type,
                                                            date=date_stamp,
                                                            location=location).order_by('-when').first()

                if best_prediction:
                    bests.append(best_prediction)
            spans_list.append(PredicionTimeSpan(type, from_date, to_date, bests, location))
        types.append(spans_list)

    return types


def future_24h_view(request, year, month, day, hour, of_what):
    context = {
        "page_title": _("Prognoza - Pogodynka"),
        "location_span_list": get_future_spans(year, month, day, hour, of_what),

    }
    return render(request, "future.html", context)


def now_24h_view(request):
    now = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    return future_24h_view(request, now.year, now.month, now.day, now.hour,
                           ["temperature", 'flux', 'wind_speed', 'wind_u', 'wind_v'])


_('temperature')
_('flux')
_('wind_speed')
_('wind_u')
_('wind_v')
