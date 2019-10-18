from time import sleep
from random import randint
def odczyt_predkosci_wiatru(_):
    v = 20 + randint(0, 10)
    print('f Predkosc:', v)
    sleep(1)
    return v


def odczyt_promieniowania(_):
    v = 20 + randint(0, 100)
    print('f Promieniowanie:', v)
    sleep(1)
    return v


def odczyt_kierunku_wiatru(_):
    v = randint(0, 359)
    print('f Kierunek:', v)
    sleep(1)
    return v