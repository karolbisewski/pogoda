import requests
from datetime import datetime
import pytemperature
import pytz
import sys
from misc import round_list
import math

sys.path.append("..")
from keys_secret import meteo_key

headers = {
    "Authorization": 'Token {}'.format(meteo_key)
}


def string_to_datetime(s):
    """
    '2019-07-11T01:00:00Z' returns datetime(2019,7,11,1,0,0, tz.info=pytz.utc)
    """
    y, m, dr = s.split('-')
    y, m = int(y), int(m)
    d = int(dr[0:2])
    rest = dr[3:-1]
    hour, minute, microsecond = map(int, rest.split(':'))
    # return datetime(year=y, month=m, day=d, hour=hour, minute=minute, microsecond=microsecond, tzinfo=pytz.UTC)
    # https://stackoverflow.com/questions/1379740/pytz-localize-vs-datetime-replace
    return pytz.utc.localize(datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ'))


def datetime_to_string(d):
    return "{}-{:02}-{:02}T{:02}".format(d.year, d.month, d.day, d.hour)


class RequestMold:
    mold = ("https://api.meteo.pl/api/v1/model/"
            "{model}/grid/{grid}/coordinates/"
            "{coordinates}/field/{field}/level/"
            "{level}/date/{date}/forecast/")
    model = "um"
    grid = None
    coordinates = "271,211"
    level = None
    field = None
    date = None

    _response = None
    name = None

    def __init__(self, date):
        self.date = date

    def _get_api_link(self):
        x = self.mold.format(model=self.model,
                             grid=self.grid,
                             coordinates=self.coordinates,
                             level=self.level,
                             field=self.field,
                             date=datetime_to_string(self.date))
        return x

    def request(self):
        self._response = requests.post(self._get_api_link(), headers=headers).json()
        if isinstance(self._response, list):
            # this means error
            r = self._response[0]
            if r == 'Given model does not exists':
                raise ValueError('Given model does not exists')
            if r == 'Given field does not exists ':
                raise ValueError(f'Given field does not exists: {self.field}')
            elif r == 'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh.':
                raise ValueError('Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh.')
            elif r == 'There is no forecast for given date.':
                raise ValueError(f'There is no {self.name} forecast for given date: {datetime_to_string(self.date)}')
            elif r == 'Hour must be one of the following values: 0, 6, 12, 18':
                raise ValueError(
                    f'Hour must be one of the following values: 0, 6, 12, 18: {datetime_to_string(self.date)}')
            else:
                raise ValueError(f"{r} {self._response}")

        return self._prepare()

    def _prepare(self):
        return list(map(string_to_datetime, self._response['times'])), self._response['data']


zapytaie = RequestMold(datetime(year=2019, month=3, day=3))


class RequestTemperature(RequestMold):
    grid = "C3"
    name = "temperature"
    field = "03236_0000000"
    level = '_'

    def __init__(self, date):
        super().__init__(date)

    def _prepare(self):
        dates, values = super()._prepare()
        return [dates, list(map(pytemperature.k2c, round_list(values, 2)))]


class RequestFlux(RequestMold):
    grid = "C3"
    name = 'flux'
    field = "01235_0000000"
    level = '_'

    def _prepare(self):
        dates, values = super()._prepare()
        return [dates, round_list(values, 3)]


class RequestWindU(RequestMold):
    grid = "p5"
    name = 'wind_u'
    field = "03225_0000000"
    level = "_"

    def _prepare(self):
        dates, values = super()._prepare()
        return [dates, round_list(values, 3)]


class RequestWindV(RequestMold):
    grid = "p5"
    name = 'wind_v'
    field = "03226_0000000"
    level = "_"

    def p_repare(self):
        dates, values = super()._prepare()
        return [dates, round_list(values, 3)]


class RequestWindSpeed():
    name = "wind_speed"

    def __init__(self, date):
        self.date = date

    def request(self):
        dates_wind_u, values_wind_u = RequestWindU(self.date).request()
        dates_wind_v, values_wind_v = RequestWindV(self.date).request()
        assert len(values_wind_u) == len(values_wind_v) and dates_wind_u == dates_wind_v
        new_speed_values = []
        for i in range(len(values_wind_v)):
            new_val = math.sqrt(values_wind_u[i] ** 2 + values_wind_v[i] ** 2)
            new_speed_values.append(new_val)

        return [dates_wind_u, new_speed_values]


def mold_abstract_factory(name):
    molds = {
        "temperature": RequestTemperature,
        "flux": RequestFlux,
        "wind_u": RequestWindU,
        "wind_v": RequestWindV,
        "wind_speed": RequestWindSpeed,
    }
    return molds[name]
