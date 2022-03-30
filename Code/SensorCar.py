from lib2to3.pgen2 import driver
import SonicCar as sc
import basisklassen as bk
import csv
import time
#import BaseCar as bc

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
        self.us = bk.Ultrasonic()
        self.fw = bk.Front_Wheels()
        self.bw = bk.Back_Wheels()
        self.turning_offset = 0

            
    def IR_poti_setting(self):
        """
            Einstellung des IR-Potis über Verstellschraube
            Ermittlung der Referenzwerte mit weißem und schwarzem Background
            Übergabe der Werte an write_to_csv
        """
        while True:
            self.ir_sens = input("Bitte Poti einstellen und Wert des Potis eingeben: ")
            self.ir = bk.Infrared()

            input('Place on background and start measurement:')
            self.background = self.ir.get_average(100)
            print('measured background:', self.background)
            input('Place on line and start measurement:')
            self.line = self.ir.get_average(100)
            print('measured line:', self.line)
            self.write_to_csv(self.ir_sens,self.background,self.line)
            stat_cal = input("Weitere Kalibrierungs-Messung? [j/n]")
            if stat_cal == "n":
                break

    
    def write_to_csv(self,ir_sens, background,line):
        """
            Übernimmt Poti-Stellung und Referenzwerte mit weißem und schwarzem Background
            Ermittelt Faktor der Sensorsummenwerte
            Schreibt Poti-Stellung, Sensorwerte weißer & schwarzer Background und Faktor Sensorsummenwerte.
        """
        with open("IR-Ref.csv", mode ='a') as log_file:
            write = csv.writer(log_file)
            sum_background = 0
            sum_line = 0
            for i in range(5):
                sum_background += background[i]
                sum_line += line[i]
            ir_sens_fact =sum_background/sum_line 
            write.writerow([ir_sens, background, line, ir_sens_fact])
            # print("CSV-Datei geschrieben")


    def test_sensoren(self):
        """
            Test der IR-Sensoren mit aktuellen Poti-Einstellungen
            Ziel: Erkennung der Linie am entsprechenden IR-Sensor
        """
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
        """
            Fahrparcours 5 ‑ Linienverfolgung : Folgen einer etwas 1,5 bis 2 cm breiten Linie auf
            dem Boden. Das Auto soll stoppen, sobald das Auto das Ende der Linie erreicht hat. Als
            Test soll eine Linie genutzt werden, die sowohl eine Rechts‑ als auch eine Linkskurve
            macht. Die Kurvenradien sollen deutlich größer sein als der maximale Radius, den das
            Auto ohne ausgleichende Fahrmanöver fahren kann.
            Zusätzlich: Hindernis-Erkennung & Stop des Fahrzeugs
        """
        
        while self.us.distance() > 5 or self.us.distance() < 0:
        
            
            sens_werte = self.ir.read_digital() #[1, 1, 0, 1, 0]  
            # print(sens_werte)
            # print(sum(sens_werte))
            if sum(sens_werte) != 0:
                lenkw_norm = (sens_werte[0]*(-1) + sens_werte[1]*(-0.5) + sens_werte[2]*0 + sens_werte[3]*0.5 + sens_werte[4]*1) / sum(sens_werte)
            else:
                lenkw_norm = 0
                break
            # print(lenkw_norm)

            lenkw_max = 45
            lenkwinkel = lenkw_norm*lenkw_max + 90

            self.drive(30, 1, lenkwinkel)
            time.sleep(0.02)
            
        
        

        
        self.stop()  

def main():
    irCar = SensorCar()
    irCar.test_sensoren()
    irCar.Fahrparcours_5()
    
    
             


if __name__ == '__main__':
    main()
