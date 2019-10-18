from django.contrib import admin
from .models import (
    TimeStamp,
    Prediction,
    PredictionType,
    Location,
)

# Register your models here.

admin.site.register(TimeStamp)
admin.site.register(Prediction)
admin.site.register(PredictionType)
admin.site.register(Location)

