from webbrowser import BackgroundBrowser
from pyparsing import java_style_comment
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
        poti_set = input("Poti-Einstellung erforderlich? [j/n]")
        if poti_set == "j":
            self.IR_poti_setting()
        self.ir = bk.Infrared()
        self.ir.cali_references()

    def IR_poti_setting(self):
            while True:
                self.ir_sens = input("Bitte Poti einstellen und Wert des Potis eingeben: ")
                self.ir = bk.Infrared()

                input('Place on background und Messung starten:')
                background = self.ir.get_average(100)
                print('measured background:', self.background)
                input('Place on line und Messung starten:')
                line = self.ir.get_average(100)
                print('measured line:', self.line)
                self.write_to_csv(self.ir_sens,background,line)
                stat_cal = input("Weitere Kalibrierungs-Messung? [j/n]")
                if stat_cal == "n":
                    break

    def write_to_csv(self,ir_sens, background,line):
        # Referenzwerte ermitteln mit weißem Background und schwarzer Line in der Mitte.
        # Schreibt Poti-Stellung, Sensorwerte und Faktor zwischen Rand- und Mittelsensor.
        # headerList = ["Sens", "D2", "D3", "D4", "D5", "D6", "Faktor"]
        with open("IR-Ref.csv", mode ='a') as log_file:
            write = csv.writer(log_file)
            sum_background = 0
            sum_line = 0
            for i in range(5):
                sum_background += background[i]
                sum_line += line[i]
            ir_sens_fact =sum_background/sum_line #self.ir._references[2] / self.ir._references[0]
            write.writerow([ir_sens, background, line, ir_sens_fact])
            #write.writerow([ir_sens,background,line,ir_sens_fact])
            


def main():
    irCar = SensorCar()


if __name__ == '__main__':
    main()
