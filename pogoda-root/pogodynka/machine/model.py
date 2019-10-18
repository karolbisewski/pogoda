
#
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import tensorflow as tf
# from sklearn.externals import joblib
# from sklearn.model_selection import TimeSeriesSplit
# import os
# from random import randint
# from itertools import islice
#
#
# Sequential = tf.keras.models.Sequential
# LSTM = tf.keras.layers.LSTM
# Flatten = tf.keras.layers.Flatten
# Dense = tf.keras.layers.Dense
# Model = tf.keras.Model
#
# from machine import (
#     get_train_test_data,
#     get_graph,
#     get_df,
#     out_scaler,
#     in_scaler,
# )
# from .data import Data
#
#
# import itertools
# import collections


def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def get_24h_predictions(prediction_name, meteo_data, politechnika_data):
    # meteo_data:  168 + 24 godzin danych z meteo
    # politechnika_data: 168 godzin danych z politechniki

    # load model
    if not os.path.exists(f'models/{prediction_name}.h5'):
        raise Exception("Wpierw wyszkol model.")
    model = load_model(f'models/{prediction_name}.h5')

    # prepare
    politechnika_data = np.array(politechnika_data)
    meteo_data = np.array(meteo_data)

    # predict 24
    predictions = []

    return [randint(0, 10) for _ in range(24)] # usunac

    for j in range(0, 24):
        meteo_current_data = np.array(meteo_data)[j, 168+j]
        politechnika_current_data = np.append(politechnika_data[j:], np.array(predictions))
        input = np.array([politechnika_current_data, meteo_current_data])
        input = np.array(input).reshape(1, 168, 2)
        y = model.predict(input)
        predictions.append(out_scaler.inverse_transform(y.flatten().reshape(-1, 1)).flatten())

    return predictions

def load_model(path):
    return tf.keras.models.load_model(path)

def create_model(prediction_name):

    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(168, 2)))
    model.add(Flatten())
    model.add(Dense(1))

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')


    i = 0
    for X_train, y_train, X_test, y_test in Data(prediction_name).get_train_test_data():
        i += 1
        X_train = X_train.reshape(X_train.shape[0], 168, 2)
        X_test = X_test.reshape(X_test.shape[0], 168, 2)
        print('--' * 10)

        model.fit(X_train, y_train, epochs=20, verbose=0)

        yhat = model.predict(X_test, verbose=0)
        # y_test = y_test.reshape(2)
        print("Test nr.", i)
        print("   SCORE:", model.evaluate(X_test, y_test))
        print('EXPECTED:', out_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten())
        print('EXPECTED:', y_test.flatten())
        print('     GOT:', out_scaler.inverse_transform(yhat.reshape(-1, 1)).flatten())
        print('     GOT:', yhat.flatten())


    X_test_day = []
    y_test_day = []

    actual = []
    pred = []
    for _X_train, _y_train, X_test, y_test in get_train_test_data():
        X_test_day.append(X_test)
        y_test_day.append(y_test)
        X_test = X_test.reshape(X_test.shape[0], 168, 2)
        y_pred = model.predict(X_test)
        actual.append(y_test)
        pred.append(y_pred)

    actual = out_scaler.inverse_transform(np.array(actual).flatten().reshape(-1, 1)).flatten()
    pred = out_scaler.inverse_transform(np.array(pred).flatten().reshape(-1, 1)).flatten()

    print(pred.shape)
    print(actual.shape)
    plt.figure(figsize=(15, 5))
    plt.title("Pomiar na Politechnice")
    plt.plot(actual)
    plt.plot(pred)
    plt.legend("Prawdziwa Przewidziana".split())
    plt.show()

    model.save(f"models/{val_name}.h5")






