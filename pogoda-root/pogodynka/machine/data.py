
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta


from pogodynka.models import (
    TimeStamp,
    Prediction,
    PredictionType,
    Location,
)
from django.conf import settings
import datetime
import pytz

class Data:
    def __init__(self, prediction_name):
        self.prediction_name = prediction_name
        self.prediction_type = PredictionType.objects.get(name=prediction_name)
        self.meteo_location = Location.objects.get(name='meteo')
        self.politechnika_location = Location.objects.get(name='politechnika')
        self._prepare_learning_data()

    def _prepare_learning_data(self):
        from_date = datetime.datetime(2019, 9, 1, tzinfo=pytz.utc)
        to_date = datetime.datetime(2019, 9, 6, tzinfo=pytz.utc)

        from_date = datetime.datetime.combine(from_date, datetime.time.min)
        to_date = datetime.datetime.combine(to_date, datetime.time.max)

        timezone = pytz.timezone(settings.TIME_ZONE)

        from_date = timezone.localize(from_date)
        to_date = timezone.localize(to_date)

        hours = TimeStamp.objects.filter(date__range=(from_date, to_date)).order_by('date')

        preds = []
        for hour in hours:
            prediction = Prediction.objects.filter(type=self.prediction_type, location=self.meteo_location, date=hour).order_by('-when').first()
            preds.append((hour.date,prediction.value))


        df1 = pd.DataFrame(preds, columns=["date", "value"])
        df1['Datetime'] = pd.to_datetime(df1['date'])
        df1 = df1.set_index('Datetime')
        df1 = df1.drop(['date'], axis=1)

        preds = []
        for hour in hours:
            prediction = Prediction.objects.filter(type=self.prediction_type, location=self.politechnika_location, date=hour).order_by('-when').first()
            preds.append((hour.date,prediction.value))


        df2 = pd.DataFrame(preds, columns=["date", "value"])
        df2['Datetime'] = pd.to_datetime(df2['date'])
        df2 = df2.set_index('Datetime')
        df2 = df2.drop(['date'], axis=1)
        #
        #
        # end_base = df1.index[-1]
        # new_dates = []
        # for _ in range(3):
        #     for i in range(df1.shape[0]):
        #         end_base += timedelta(hours=1)
        #         new_dates.append(pd.to_datetime(end_base))
        #
        # new_values = []
        # bias = 0
        # bias2 = 0
        # for _ in range(3):
        #     for i in range(df1.shape[0]):
        #         bias += (np.random.random_sample() - 0.5) / 5
        #         bias2 += (np.random.random_sample() - 0.5) / 1
        #         new_values.append(df1['value'][i] + df1['value'][i]/3 + bias  - np.random.random_sample())
        # n = pd.DataFrame(new_values,
        #                               index=new_dates,
        #                  columns=['value'])
        # df1 = df1.append(n)


        # df2 = df1.copy()
        # df2['value'] += np.random.randint(-10,-5,df1.shape[0])/9

        df1.columns = ["meteo"]
        df2.columns = ["politechnika"]


        ax = df1.plot()
        df2.plot(ax=ax)

        df1['politechnika'] = df2['politechnika']

        shift_days = 1
        warump_days = 6

        warump_steps = warump_days * 24
        shift_steps = shift_days * 24 # 144,  hours

        df = df1.copy()

        politechnika = df["politechnika"].values[:-168]
        meteo = df["meteo"].values[24:-144]
        data_in = [politechnika, meteo]
        data_out = df["politechnika"].values[144:-24]


        in_scaler = MinMaxScaler()
        out_scaler = MinMaxScaler()

        self.tscv = TimeSeriesSplit((len(data_out)-1)//4)
        self.in_scaled = in_scaler.fit_transform(data_in)
        self.out_scaled = out_scaler.fit_transform(data_out.reshape(-1,1)).flatten()

    def get_train_test_data(self):
        print("GETTING DATA")
        for train_index, test_index in self.tscv.split(self.out_scaled[:-168]):
            # print("TRAIN:", train_index, "TEST:", test_index)
            X_train = []
            y_train = []

            for i in train_index:
                train_start = i
                train_end = i + 168
                _X_train = np.array(self.in_scaled)[:, train_start: train_end]
                _y_train = self.out_scaled[i]

                X_train.append(_X_train)
                y_train.append(_y_train)
            X_train = np.array(X_train)
            y_train = np.array(y_train)

            X_test = []
            y_test = []
            for i in test_index:
                test_start = i
                test_end = i + 168
                _X_test = np.array(self.in_scaled)[:,test_start: test_end]
                _y_test = np.array(self.out_scaled[i])
                X_test.append(_X_test)
                y_test.append(_y_test)

            # for a in X_test:
            #     print(a.shape)
            X_test = np.array(X_test)
            y_test = np.array(y_test)
            # print("RETURNING TRAIN", X_train.shape, y_train.shape)
            # print("RETURNING TEST", X_test.shape, y_test.shape)
            yield X_train, y_train, X_test, y_test


