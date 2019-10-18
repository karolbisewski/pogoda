"""pogoda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pogodynka.views import (
    date_view,
    dates_view,
)
from pogodynka.actuall_view import (
    future_24h_view,
    now_24h_view,
)
from pogodynka.api_views import (
    api_date_for_day_view,
    api_get_future_graph,
)
from pages.views import (
    homepage_view,
)
from pogodynka.politechnika.views import (
    readings_view,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dates/', dates_view),
    path('api/live_readings/', readings_view),
    path('future/<int:year>-<int:month>-<int:day>/<int:hour>/<str:of_what>', future_24h_view),
    path('future/', now_24h_view),
    path('api/date/<int:year>/<int:month>/<int:day>/', api_date_for_day_view),
    path('api/future-graph/<int:year>/<int:month>/<int:day>/<int:hour>/<str:of_what>',
        api_get_future_graph),
    path('date/<int:year>-<int:month>-<int:day>/<int:hour>', date_view),
    path('', homepage_view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
