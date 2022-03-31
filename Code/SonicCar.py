import BaseCar as bc
import time
from datetime import datetime
import csv
import pandas as pd

class SonicCar(bc.BaseCar):
# class SonicCar:
    """
    Eine Klasse SonicCar soll die Eigenschaften der Klasse BaseCar
    erben und zusätzlich den Zugriff auf den Ultraschall‑Sensor ermöglichen. Die Fahrdaten
    umfassen die Geschwindigkeit, die Fahrtrichtung, den Lenkwinkel und die Daten des
    Ultraschall‑Sensors. Dazu soll Folgendes entwickelt und getestet werden.
    """

    def __init__(self):
        self.fw = bc.bk.Front_Wheels()
        self.bw = bc.bk.Back_Wheels()
        self.us = bc.bk.Ultrasonic()
        self._abstand = 5
        self.global_data =[]
        self.car_calibration()

    @property
    def abstand(self):
         return self._abstand

    @abstand.setter
    def abstand(self, abstand):
        if abstand > 0:
            self._abstand = abstand
        else:
            print("Fehler")

    def driving_data(self,dist):
        t_now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        return (t_now,self.speed,self.direction,self.steering_angle,dist)
    
    def write_to_csv(self):
        headerList =["t_now","speed","direction","steering_angle","distance"] 
        with open("Log-Datei.csv", mode ='w') as log_file:
            write = csv.writer(log_file)
            write.writerow(headerList)
            write.writerows(self.global_data)    
    
    def obstacle(self):
        """
        Ermittelt Abstand und unterbricht bei Wert < "abstand"
        """
        
        while True:
            time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)
            if dist > 0 and dist <= self.abstand:
                print("Achtung!", dist, "cm")
                self.stop()
                break
    
    # def data_rec(self):
    #    while True:
    #         time.sleep(0.1)
    #         dist = self.us.distance()
    #         data = self.driving_data(dist)
    #         self.global_data.append(data)
    #         break
   

    def Fahrparcours_3(self) -> None:        
        self.drive(50, 1, 90)
        
        print(self.speed)
        self.obstacle()

    def RW(self) -> None:        
         self.drive(30, -1, 135)
         for i in range(30):
             time.sleep(0.1)
             dist = self.us.distance()
             data = self.driving_data(dist)
             self.global_data.append(data)

    def FW_slow(self) -> None:   
        self.drive(30, 1, 90)
        for i in range(40):
            time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)

        self.drive(30, 1, 135)
        for i in range(20):
            time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)

        self.drive(30, 1, 45)
        for i in range(20):
            time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)   

    def Fahrparcours_4(self) -> None:
        #while True:
        self.abstand = self.abstand
        self.Fahrparcours_3()  
        self.RW()
        #self.FW_slow() 
        self.Fahrparcours_3()
        self.write_to_csv()
        
        
def main():
    sc = SonicCar()
    sc.Fahrparcours_4()
    sc.write_to_csv()

if __name__ == '__main__':
    main()