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
    # def __init__(self, speed: int = 0, direction: int = 0, steering_angle: int = 90):
    #     super().__init__(speed, direction, steering_angle)

    def __init__(self):
        # super().__init__(speed, direction, steering_angle)
        # super().__init__()

        # self._speed = 0
        # self._direction = 0
        # self._steering_angle = 90
        self.fw = bc.bk.Front_Wheels()
        self.bw = bc.bk.Back_Wheels()
        self.us = bc.bk.Ultrasonic()
        self._too_close = 10
        self.global_data =[]

    # #@property
    # def too_close(self):
    #     return self._too_close

    #@too_close.setter
    def mt_too_close(self, speed, factor: int = 1):
            self.too_close = int(factor*(speed/3))

    def driving_data(self,dist):
        t_now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        return (t_now,self.speed,self.direction,self.steering_angle,dist)
    
    def write_to_csv(self):
        headerList =["t_now","speed","direction","steering_angle","distance"] 
        with open("Log-Datei.csv", mode ='w') as log_file:
            write = csv.writer(log_file)
            write.writerow(headerList)
            write.writerows(self.global_data)    
    
    def obstacle(self, too_close):
        """
        Ermittelt Abstand und unterbricht bei Wert < "too_close"
        """
        #self.global_data =[] 
        while True:
            bc.bk.time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)
            if dist > 0 and dist < too_close:
                print("Achtung!", dist, "cm")
                self.stop()
                break
    
    def data_rec(self):
       while True:
            time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)
            break
   

    def Fahrparcours_3(self) -> None:        
        self.drive(60, 1, 90)
        #self.too_close = -4
        print(self.speed)
        print(type(self.speed))
        self.mt_too_close(self.speed)
        #too_close = self.speed/3
        #print(self.too_close)
        self.obstacle(self.too_close)

    def RV(self) -> None:        
        self.drive(30, -1, 135)
        for i in range(20):
            time.sleep(0.1)

            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)           
        

    def Fahrparcours_4(self) -> None:   
        #self.data_rec()
        self.Fahrparcours_3()
        #self.drive(30, -1, 135)
        self.RV()
        #time.sleep(2)
        #self.stop()        
        self.Fahrparcours_3()
        #self.drive(30, 1, 90)
        
def main():
    
    sc = SonicCar()
    sc.Fahrparcours_4()
    sc.write_to_csv()

if __name__ == '__main__':
    main()