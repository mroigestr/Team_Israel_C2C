#coding=utf-8
#!/usr/bin/env python

"""
Dieses Programm nutzt nur Basisklassen.py!
"""
print('Hallo! Das ist ein Test')
print('RPiCar grüßt durch Wackeln mit den Vorderrädern!')
from basisklassen import  *
import traceback

n=.3

try:
    #Wackeln mit den Vorderrädern als Gruß
    fw=Front_Wheels()
    fw.turn(90)
    time.sleep(1)
    fw.turn(45)
    time.sleep(n)
    fw.turn(135)
    time.sleep(n)
    fw.turn(90)
    time.sleep(n)
    fw.turn(135)
    time.sleep(n)
    fw.turn(45)
    time.sleep(n)
    fw.turn(90)
    time.sleep(1)
    
except:
    print('-- FEHLER --')
    print(traceback.format_exc())
