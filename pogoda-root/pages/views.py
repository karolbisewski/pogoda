from django.shortcuts import render
from django.utils.translation import gettext as _
# Create your views here.


def homepage_view(request):

    context = {
        "page_title": _('Forecaster')
    }
    return render(request, 'home.html', context)