# import sys

from django.utils import timezone


try:
    from politechnika.reader import (
        odczyt_predkosci_wiatru,
        odczyt_kierunku_wiatru,
        odczyt_promieniowania,
    )
except ModuleNotFoundError:
    from politechnika.fake_reader import (
        odczyt_predkosci_wiatru,
        odczyt_kierunku_wiatru,
        odczyt_promieniowania,
    )
    
from active import create_politechnika_Prediction
from misc import get_current_date_hour

def save():
    print("Saving politechnka predictions...")
    create_Prediction('wind_speed', odczyt_predkosci_wiatru(20))
    create_Prediction('flux', odczyt_promieniowania(20))
    # DODAC --
    # create_Prediction('wind_dir', odczyt_kierunku_wiatru(10))
    print("Politechnika saving done.")
    print('-' * 10)
    print()


def create_Prediction(type, value):
    print(get_current_date_hour())
    create_politechnika_Prediction(type, get_current_date_hour(), value)


def show():
    odczyt_predkosci_wiatru(2)
    odczyt_kierunku_wiatru(2)
    odczyt_promieniowania(2)
    print('-' * 10)
    print()


if __name__ == '__main__':
    while True:
        show()
