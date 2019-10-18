import unittest
import mold
from datetime import datetime
import pytz
import requests


class TestMold(unittest.TestCase):
    def test_datetime_to_string(self):
        self.assertEqual("2019-12-13T10", mold.datetime_to_string(datetime(2019, 12, 13, 10, tzinfo=pytz.UTC)))
        self.assertEqual("2019-07-11T01", mold.datetime_to_string(datetime(2019, 7, 11, 1, tzinfo=pytz.UTC)))
        self.assertEqual("2019-12-13T10", mold.datetime_to_string(datetime(2019, 12, 13, 10, 1, tzinfo=pytz.UTC)))
        self.assertEqual("2018-01-04T07", mold.datetime_to_string(datetime(2018, 1, 4, 7, tzinfo=pytz.utc)))

    def test_string_to_datetime(self):
        self.assertEqual(
            datetime(2019, 12, 13, 10, tzinfo=pytz.UTC), mold.string_to_datetime("2019-12-13T10:00:00Z"), )
        self.assertEqual(
            datetime(2019, 7, 11, 1, tzinfo=pytz.UTC), mold.string_to_datetime("2019-07-11T01:00:00Z"), )
        self.assertEqual(
            datetime(2019, 12, 13, 10, 1, tzinfo=pytz.UTC), mold.string_to_datetime("2019-12-13T10:01:00Z"))
        self.assertEqual(
            datetime(2019, 12, 4, 4, 1, tzinfo=pytz.UTC), mold.string_to_datetime("2019-12-04T04:01:00Z"))

    def test_request(self):
        n = mold.RequestMold(datetime(2019, 11, 10, tzinfo=pytz.utc), 'temperature')
        self.assertEqual((
            'https://api.meteo.pl/api/v1/model/coamps/grid/2a/coordinates/84,116/'
            'field/grdtmp_sfc_fcstfld/level/000000_000000/date/2019-11-10T00/forecast/'
        ), n._get_api_link())
        n = mold.RequestMold(datetime(2018, 1, 4, 7, tzinfo=pytz.utc), 'temperature')
        self.assertEqual((
            'https://api.meteo.pl/api/v1/model/coamps/grid/2a/coordinates/84,116/'
            'field/grdtmp_sfc_fcstfld/level/000000_000000/date/2018-01-04T07/forecast/'
        ), n._get_api_link())

    def test_meteo_connection(self):
        self.assertEqual({
            'models': ['coamps', 'um', 'wrf']},
            requests.get("https://api.meteo.pl/api/v1/model/", headers=mold.headers).json())


if __name__ == '__main__':
    unittest.main()
