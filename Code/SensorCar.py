import SonicCar as sc
import basisklassen as bk

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
        self.ir.cali_references()
        # print("In def __init__")
        # print(self.ir._references)


def main():
    irCar = SensorCar()
    # print(irCar.background)

if __name__ == '__main__':
    main()
