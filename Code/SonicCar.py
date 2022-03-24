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


    @property
    def too_close(self):
        return self._too_close

    # @too_close.setter
    # def too_close(self, too_close):
    #     if too_close < 10:
    #         print("Warnwert muss >= 10 sein und nicht {}!".format(too_close))
    #         print("Warnwert wird auf 10 cm gesetzt!")
    #         self._too_close = 10
    #     else:
    #         self._too_close = too_close


    def too_close(self, speed):
        self.too_close = speed/3


    def driving_data(self,dist):
        t_now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        return (t_now,self.speed,self.direction,self.steering_angle,dist)
    
    def write_to_csv(self):
        headerList =["t_now","speed","direction","steering_angle","distance"] 
        with open("Log-Datei.csv", mode ='w') as log_file:
            write = csv.writer(log_file)
            write.writerow(headerList)
            write.writerows(self.global_data)

 
        # #import os
        # headers = ['head1', 'head2']
        # for row in interator:
        #     with open('file.csv', 'a') as f:
        #         file_is_empty = os.stat('file.csv').st_size == 0
        #         writer = csv.writer(f, lineterminator='\n')
        #         if file_is_empty:
        #             writer.writerow(headers)
        #         writer.writerow(row)


        
        # display csv file
        
    
    
    def obstacle(self, too_close):
        """
        Ermittelt Abstand und unterbricht bei Wert < "too_close"
        """
        self.global_data =[] 
        while True:
            bc.bk.time.sleep(0.1)
            dist = self.us.distance()
            data = self.driving_data(dist)
            self.global_data.append(data)
            if dist > 0 and dist < too_close:
                print("Achtung!", dist, "cm")
                self.stop()
                break



    
    def Fahrparcours_3(self) -> None:

        self.drive(60, 1, 90)
        #self.too_close = -4
        self.too_close(self.speed)
        print(self.too_close)
        self.obstacle(self.too_close)

        
def main():
    sc = SonicCar()
    sc.Fahrparcours_3()
    sc.write_to_csv()


if __name__ == '__main__':
    main()
