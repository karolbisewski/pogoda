from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.conf import settings
from .models import (
    TimeStamp,
)
from .actuall_view import get_future_spans
from .templatetags import graph_extras
import datetime
import pytz
from django.template import loader
from django.http import HttpResponse

def api_date_for_day_view(request, year, month, day):
    """Returns list of dates (time_stamp) for that day with are in the database in json"""
    from_date = datetime.datetime(year, month, day, tzinfo=pytz.utc)
    from_date = datetime.datetime.combine(from_date, datetime.time.min)
    to_date = datetime.datetime.combine(from_date, datetime.time.max)

    timezone = pytz.timezone(settings.TIME_ZONE)

    from_date = timezone.localize(from_date)
    to_date = timezone.localize(to_date)
    hours = TimeStamp.objects.filter(date__range=(from_date, to_date)).order_by('date')

    hours = [hour.date for hour in hours]
    return JsonResponse(hours, safe=False)


def api_get_future_graph(request, year, month, day, hour, of_what):
    print(1)
    template = loader.get_template('complete-standard-future.html')
    types_list = get_future_spans(year, month, day, hour, of_what)
    print(types_list)
    context = {
        "location_span_list": types_list
    }

    return HttpResponse(template.render(context), request)
