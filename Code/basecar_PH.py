import basisklassen as bk
import click
import time
import numpy as np
import math
import RPi.GPIO as GPIO
import smbus
import json




class BaseCar:
    """
    Entwicklung und Testen einer Klasse BaseCar mittels der Basisklassen
    mit vorgegebenen Anforderungen. Die Klasse soll folgende Attribute (mit entsprechen‑
    den Gettern und Settern) und Methoden haben:
    • steering_angle: Zugriff auf den Lenkwinkel
    • drive(int, int): Fahren mit übergebener Geschwindigkeit und Fahrrichtung
    • stop(): Anhalten des Autos
    • speed: Zugriff auf die Geschwindigkeit
    • direction: Zugriff auf die Fahrrichtung (1: vorwärts, 0: Stillstand, ‑1 Rückwärts)
    Die Klasse BaseCar soll mittels folgenden Aufgaben getestet werden.
    """
    def __init__(self, steering_angle: int = 0, speed: int = 0, direction: int = 0):
        self._steering_angle = steering_angle
        self._speed = speed
        self._direction = direction
        self.bw = bk.Back_Wheels()
        self.fw = bk.Front_Wheels()

    @property 
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        self._speed = speed

    @property
    def steering_angle(self):
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, steering_angle):
        self._steering_angle = steering_angle

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction
    
    def drive(self, speed: int = 0, direction: int = 0, steering_angle: int = 90):
        self.bw.speed = speed
        self.speed = speed
        self.direction = direction
        self.steering_angle = steering_angle

        self.fw.turn(steering_angle)
        if direction == 1:
            self.bw.forward()
        elif direction == -1:
            self.bw.backward()
    
    def stop(self):
        self.speed = 0
        self.bw.speed = self.speed

    def Fahrparcours_1(self):
        """
        Fahrparcours 1 - Vorwärts und Rückwärts: Das Auto fährt mit langsamer Geschwindigkeit
        3 Sekunden geradeaus, stoppt für 1 Sekunde und fährt 3 Sekunden rückwärts.
        """
        self.speed = 40
        self.direction = 1

        self.drive(self.speed, self.direction)
        time.sleep(3)
        self.stop()
        time.sleep(1)
        self.speed = 40
        self.direction = -1
        self.drive(self.speed, self.direction)
        time.sleep(3)
        self.stop()

    def Fahrparcours_2(self):
        """
        Kreisfahrt mit maximalem Lenkwinkel: Das Auto fährt 1 Sekunde
        geradeaus, dann für 8 Sekunden mit maximalen Lenkwinkel im Uhrzeigersinn und stoppt.
        Dann soll das Auto diesen Fahrplan in umgekehrter Weise abfahren und an den Ausgangspunkt
        zurückkehren. Die Vorgehensweise soll für eine Fahrt im entgegengesetzten
        Uhrzeigersinn wiederholt werden.
        """
        # Vorwärts, geradeaus für 1s
        self.drive(40,1,90)
        time.sleep(1)
        print("Part1")
        # Vorwärts, max. Lenkeinschlag nach rechts für 8s
        self.drive(60,1,135)
        time.sleep(8)
        # 1s Stop
        self.stop()
        time.sleep(1)
        # Rückwärts, max. Lenkeinschlag nach rechts für 8s
        self.drive(40,-1,135)
        time.sleep(8)
        # Rückwärts, geradeaus für 1s
        self.drive(40,-1,90)
        time.sleep(1)
        # Stop
        self.stop()
        

def main():
    #bk()
    #bw = bk.Back_Wheels()
    bc = BaseCar()
    #bc.Fahrparcours_1()
    bc.Fahrparcours_2()
    #bw.test()
    print("Fahrparcours_1 gefahren")

if __name__ == "__main__":
    main()