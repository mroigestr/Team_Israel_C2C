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
        ir_sens_cali = input("IR-Sensoren kalibrireren? [j/n]: ")
        if ir_sens_cali == "j":
            self.ir.cali_references()
            self.write_to_csv()
        # print("In def __init__")
        # print(self.ir._references)

    def write_to_csv(self):
        # Referenzwerte ermitteln mit weißem Background und schwarzer Line in der Mitte.
        # Schreibt Poti-Stellung, Sensorwerte und Faktor zwischen Rand- und Mittelsensor.
        # headerList = ["Sens", "D2", "D3", "D4", "D5", "D6", "Faktor"]
        with open("IR-Ref.csv", mode ='a') as log_file:
            write = csv.writer(log_file)
            ir_sens = input("IR-Poti [1...3]: ")
            # write.writerow(headerList)
            ir_sens_fact = self.ir._references[2] / self.ir._references[0]
            write.writerow([ir_sens, self.ir._references, ir_sens_fact])


def main():
    irCar = SensorCar()


if __name__ == '__main__':
    main()
