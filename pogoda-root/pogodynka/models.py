from django.db import models
from django.utils.timezone import localtime


class TimeStamp(models.Model):
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date)

    @property
    def get_year(self):
        return localtime(self.date).year

    @property
    def get_month(self):
        return localtime(self.date).month

    @property
    def get_day(self):
        return localtime(self.date).day

    @property
    def get_hour(self):
        return localtime(self.date).hour

    @property
    def get_slug(self):
        y, m = self.get_year, self.get_month
        d, h = self.get_day, self.get_hour
        return f"{y}-{m}-{d}/{h}"


class PredictionType(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Prediction(models.Model):
    # w wtorek utworzymy prognozę, że w czwartek będzie ciepło, to znaczy, że
    # when = wtorek
    # date = czwartek
    when = models.DateTimeField()  # creation time
    value = models.FloatField()
    type = models.ForeignKey(PredictionType, on_delete=models.DO_NOTHING)
    date = models.ForeignKey(TimeStamp, on_delete=models.CASCADE)  # dotyczy
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {} {}'.format(self.type, round(self.value, 2), self.date, self.location)


class PredicionTimeSpan:
    def __init__(self, prediction_type, start_stamp, end_stamp, predictions, location):
        self.prediction_type = prediction_type
        self.type = prediction_type
        self.location = location
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp
        self.predictions = predictions
