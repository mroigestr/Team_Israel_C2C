from lib2to3.pgen2 import driver
import SonicCar as sc
import basisklassen as bk
import csv

class SensorCar(sc.SonicCar):

    """
    Die Klasse SensorCar soll zusätzlich den Zugriff auf die Infrarot‑Sensoren ermöglichen. 
    Mittels dieser Sensoren soll das Auto in die Lage versetzt werden eine Linie auf dem Boden 
    zu erkennen. Die Daten der Infrarotsenoren sollen ebenfalls aufgezeichet werden. 
    Anmerkung: Die Sensitivität der Infrarotsensoren kann durch das blaue Potentiometer 
    eingestellt werden. Dies kann zur erheblichen Verbesserung der Ergebnisse führen.
    """

    def __init__(self):
        self.ir = bk.Infrared()
        self.us = bk.Ultrasonic()
        ir_sens_cali = input("IR-Sensoren kalibrireren? [j/n]: ")
        if ir_sens_cali == "j":
            self.ir_sens = input("IR-Poti stellen und eingeben [1...3]: ")
            self.ir.cali_references()
            # self.write_to_csv()

    def write_to_csv(self):
        # Referenzwerte ermitteln mit weißem Background und schwarzer Line in der Mitte.
        # Schreibt Poti-Stellung, Sensorwerte und Faktor zwischen Rand- und Mittelsensor.
        # headerList = ["Sens", "D2", "D3", "D4", "D5", "D6", "Faktor"]
        with open("IR-Ref.csv", mode ='a') as log_file:
            write = csv.writer(log_file)
            # write.writerow(headerList)
            ir_sens_fact = self.ir._references[2] / self.ir._references[0]
            write.writerow([self.ir_sens, self.ir._references, ir_sens_fact])

    # def steer_line(self):
    #     self.ir.read_digital()

"""    def Fahrparcours_5(self) -> None:
        while True:
            self.drive(10, 1, 90)
            sensor_lesen
            turn()"""
        
       

def main():
    irCar = SensorCar()
    input()
    print(irCar.ir.read_digital())


if __name__ == '__main__':
    main()
