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
        self.dir = bk.Front_Wheels()
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

    def test_sensoren(self):
        antwort = input('Sensoren testen?[j/n]: ')
        if antwort == "j":
            input("1. Sensor (von links ab)")
            print(self.ir.read_digital())
            print(self.ir.read_analog())
            input("2. Sensor (von links ab)")
            print(self.ir.read_digital())
            print(self.ir.read_analog())
            input("3. Sensor (von links ab)")
            print(self.ir.read_digital())
            print(self.ir.read_analog())
            input("4. Sensor (von links ab)")
            print(self.ir.read_digital())
            print(self.ir.read_analog())
            input("5. Sensor (von links ab)")
            print(self.ir.read_digital())
            print(self.ir.read_analog())
        

    def Fahrparcours_5(self):
        while True:
            self.drive(10, 1, 90)
            ist_stand_sensoren = self.ir.read_digital()
            soll_stand_sensoren = [0, 0, 1, 0, 0]
            """
            insgesamt 2**5 = 32 mögliche ausgaben
            Fall_1 --> [1, 0, 0, 0, 0] ---> links abbiegen --> lenkwinkel auf 45 setzen
            ...
            Fall_3 --> [0, 0, 1, 0, 0] --> geradeaus fahren -->lenkwinkel auf 90 setzen 
            ...
            Fall_5 --> [0, 0, 0, 0, 1] ---> rechts abbiegen --> lenkwikel auf 135 setzen
            """
            dict_infrared_werte = {}
             
            for i in range(32):
                bnr = (bin(i).replace('0b',''))
                x = bnr[::-1]
                while len(x) < 5:
                    x += '0'
                bnr = x[::-1]
                dict_infrared_werte[bnr] = "Fall {}".format(i+1)

def main():
    irCar = SensorCar()
    irCar.test_sensoren()
    dict_infrared_werte = {}
             
    for i in range(32):
        bnr = (bin(i).replace('0b',''))
        x = bnr[::-1]
        while len(x) < 5:
            x += '0'
        bnr = x[::-1]
        dict_infrared_werte[bnr] = "Fall {}".format(i+1)

    print(dict_infrared_werte)




if __name__ == '__main__':
    main()
