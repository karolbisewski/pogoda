import time
import Adafruit_ADS1x15
from time import sleep
nachylenie=0.05
adc = Adafruit_ADS1x15.ADS1115()
zakres_czujnika_kierunku = 5
zakres_przetwornika = 4.096
value_promieniowanie1 = 0
value_promieniowanie2 = 0
promieniowanie_suma = 0.0
kierunek_suma = 0.0 
predkosc_suma = 0.0

predkosc_wiatru = 0
while True:
    #pętla do próbkowania 
    for i in range(0, 200):
        #kierunek wiatru 
        kierunek_suma = kierunek_suma + ((adc.read_adc(1, 1)/1000) / zakres_przetwornika) * (360 / zakres_czujnika_kierunku)
        #promieniowanie 
        test_promieniowanie1 = adc.read_adc(2, 1)
        test_promieniowanie2 = adc.read_adc(3, 1)
    
        promieniowanie1 = (value_promieniowanie1/4092)*1000/68
        promieniowanie2 = (value_promieniowanie2/4092)*1000/68
    
        promieniowanie_suma = promieniowanie_suma + abs(promieniowanie1-promieniowanie2)
        #kierunek wiatru 
        test_predkosc_wiatru = adc.read_adc(0, 1)
        if test_predkosc_wiatru < 2000:
            predkosc_suma = predkosc_suma + ((test_predkosc_wiatru/1000)/zakres_przetwornika) * (75/5)
    #srednia wartosc z 50 probek     
    promieniowanie = round(promieniowanie_suma/200, 1)
    predkosc_wiatru = round(predkosc_suma/200, 1)
    kierunek_wiatru = round(kierunek_suma/200, 1)
    
    promieniowanie_suma = 0.0
    kierunek_suma = 0.0 
    predkosc_suma = 0.0
    #odczyt energii z pliku 

    #obliczanie energii wyprodukowanej przez wiatr
    from datetime import datetime
    czas = datetime.now().strftime("%H:%M:%S")

    
    logfile = open('predkosc_wiatru.txt', 'a')
    logfile.write("{}-{}\n".format(czas, predkosc_wiatru))
    logfile.close()
    
    logfile = open('kierunek_wiatru.txt', 'a')
    logfile.write("{}-{}\n".format(czas, kierunek_wiatru))
    logfile.close()
    
    logfile = open('promieniowanie.txt', 'a')
    logfile.write("{}-{}\n".format(czas, promieniowanie))
    logfile.close()
    
     

    print('predkosc wiatru:', predkosc_wiatru)
    print('kierunek wiatru:', kierunek_wiatru)
    print('promieniwanie:', promieniowanie)
    print('-'*10)
    time.sleep(2)
    


