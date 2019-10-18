import Adafruit_ADS1x15

from time import sleep
import time

adc = Adafruit_ADS1x15.ADS1015()
ADC_MAX_VALUE = 2 ** 11 - 1  # not 2**12, because the adc can read negative numbers.
ADC_BASE_GAIN_VOLTAGE = 4.096

preds = []

def srednia(lst):
    return sum(lst) / len(lst)


# --

def wartosc_do_napiecia(wartosc, wzmocnienie=1.0):
    return (wartosc * (ADC_BASE_GAIN_VOLTAGE / wzmocnienie)) / ADC_MAX_VALUE


def napiecie_do_wartosci(napiecie, wzmocnienie=1.0):
    return int(napiecie * ADC_MAX_VALUE / (ADC_BASE_GAIN_VOLTAGE / wzmocnienie))


# --
def odczyt_napiecia(wartosc, wzmocnienie=1.0):
    return wartosc_do_napiecia(adc.read_adc(wartosc, wzmocnienie), wzmocnienie)


def odczyt_promieniowania(okres):
    probki = []

    plusy = []
    minusy = []

    start_zegara = time.time()
    while time.time() < start_zegara + okres:
        __plus = max(odczyt_napiecia(2, 2/3), 0) # musi być dodatnie
        __minus = max(odczyt_napiecia(3, 2/3), 0) # musi być dodatnie
        _plus = __plus * (10 ** 3)
        _minus = __minus * (10 ** 3)

        plusy.append(_plus)
        minusy.append(_minus)

        probki.append(max(_plus - _minus, 0))
        sleep(0.02)

    napiecie = srednia(probki)
    naslonecznienie = napiecie / 68

    print('Nasłonecznienie - {:.2f} W/m2'.format(naslonecznienie))
    print("Nasłonecznienie - napięcie: {:.2f} mV".format(napiecie))
    print("Nasłonecznienie - Ilosc próbek:", len(probki))
    return naslonecznienie


def odczyt_predkosci_wiatru(okres):
    # https://github.com/adafruit/Adafruit_Python_ADS1x15/blob/master/examples/comparator.py

    nachylenie = 0.05  # m
    przesuniecie = 0.3  # m/s
    adc.start_adc_comparator(0,
                             napiecie_do_wartosci(4),  # High threshold
                             napiecie_do_wartosci(2),  # Low threshold
                             gain=1,
                             active_low=True,
                             latching=True)  # could be false, but i don't care.
    impulsy = 0
    block = False
    srodkowa_wartosc = napiecie_do_wartosci(3)

    start_zegara = time.time()
    while time.time() <= start_zegara + okres:
        probka = adc.get_last_result()
        if not block and probka < srodkowa_wartosc:
            impulsy += 1
            block = True
        if block and probka >= srodkowa_wartosc:
            block = False
        sleep(0.0001)
    koniec_zegara = time.time()

    czestotliwosc = impulsy / (koniec_zegara - start_zegara)
    predkosc = czestotliwosc * nachylenie + przesuniecie

    print('Prędkość - {:.2f} m/s'.format(predkosc))
    print('Prędkość - Częstotliwość: {:.2f} Hz'.format(czestotliwosc))
    return predkosc


def odczyt_kierunku_wiatru(okres):
    kierunki = []

    end = time.time()
    while time.time() < end + okres:
        napiecie = odczyt_napiecia(1, 2 / 3)
        kierunki.append(360 * napiecie / 5)
        sleep(0.02)

    kierunek = srednia(kierunki)
    print('Kierunek - {:.2f}°'.format(kierunek))
    print("Kierunek - Ilość próbek:", len(kierunki))
    return kierunek
