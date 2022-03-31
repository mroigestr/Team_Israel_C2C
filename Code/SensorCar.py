import basisklassen as bk
# import BaseCar as bc
import SonicCar as sc
import csv
import time
# from lib2to3.pgen2 import driver

class SensorCar(sc.SonicCar):
    """
        Die Klasse SensorCar soll zusätzlich den Zugriff auf die Infrarot‑Sensoren ermöglichen. 
        Mittels dieser Sensoren soll das Auto in die Lage versetzt werden eine Linie auf dem Boden 
        zu erkennen. Die Daten der Infrarotsenoren sollen ebenfalls aufgezeichet werden. 
        Anmerkung: Die Sensitivität der Infrarotsensoren kann durch das blaue Potentiometer 
        eingestellt werden. Dies kann zur erheblichen Verbesserung der Ergebnisse führen.
    """

    def __init__(self):
        self.bw = bk.Back_Wheels()
        self.fw = bk.Front_Wheels()
        self.us = bk.Ultrasonic()
        self.ir = bk.Infrared()
        self.turning_offset = 0
        poti_set = input("Poti-Einstellung erforderlich? [j/n]: ")
        if poti_set == "j":
            self.IR_poti_setting()
        self.ir.cali_references() # In if-Block setzen? Dann Eintrag der Werte in config.json.
        self.lenkw_max = 45 # Betrag des max. Lenkwinkeleinschlags.
        self.lenkw_norm = 0 # Normierten Lenkwinkeleinschlag im Intervall [-1, +1] vorbelegen auf 0.
        self.bg_line = input("""Bitte Boden- & Linienespezifikation definieren
                            Heller Untergrund/dunkle Linie -> Insert 0
                            Dunkler Untergrund/helle Linie -> Insert 1
                            """)
            
    def IR_poti_setting(self):
        """
            Einstellung des IR-Potis über Verstellschraube.
            Ermittlung der Referenzwerte mit Hintergrund und Linienfarbe.
            Übergabe der Werte an write_to_csv.
        """
        while True:
            self.ir_sens = input("Bitte Poti einstellen und Wert des Potis eingeben: ")
            self.ir = bk.Infrared() # Steht schon in __init__!?!

            input("Place on background and start measurement: ")
            self.background = self.ir.get_average(100)
            print("measured background: ", self.background)
            input("Place on line and start measurement: ")
            self.line = self.ir.get_average(100)
            print("measured line: ", self.line)
            self.write_to_csv(self.ir_sens, self.background, self.line)
            stat_cal = input("Weitere Kalibrierungs-Messung? [j/n]: ")
            if stat_cal == "n":
                break

    
    def write_to_csv(self, ir_sens, background, line):
        """
            Übernimmt Poti-Stellung und Referenzwerte mit Hintergrund und Linienfarbe.
            Ermittelt Faktor der Sensorsummenwerte.
            Schreibt Poti-Stellung, Sensorwerte Hintergrund, Linienfarbe, Faktor Sensorsummenwerte.
        """
        with open("IR-Ref.csv", mode = "a") as log_file:
            write = csv.writer(log_file)
            sum_background = 0
            sum_line = 0
            for i in range(len(line)): # Schleife ueber alle Sensoren.
                sum_background += background[i]
                sum_line += line[i]
            ir_sens_fact = sum_background / sum_line 
            write.writerow([ir_sens, background, line, ir_sens_fact])
            # print("CSV-Datei geschrieben.")

    def invert_digital_val(self, sens_werte):
        # Create a Dictionary for digital inversion
        b_dict = {0: 1, 1: 0}
        self.sens_werte_invert = []
        #sens_val = self.ir.read_digital()

        for i in sens_werte:
            self.sens_werte_invert.append(b_dict[i])
        return self.sens_werte_invert
        print(self.sens_werte_invert)

    def test_sensoren(self):
        """
            Test der IR-Sensoren mit aktuellen Poti-Einstellungen.
            Ziel: Erkennung der Linie am entsprechenden IR-Sensor.
        """
        antwort = input("IR-Sensoren testen? [j/n]: ")
        if antwort == "j":
            for i in range(5):
                input(str(i+1) + ". Sensor (von links)")
                if self.bg_line == "0":
                    val_digital = self.ir.read_digital()
                elif self.bg_line == "1":
                    val_digital = self.invert_digital_val(self.ir.read_digital())
                val_analog = self.ir.read_analog()
                print(val_digital)
                print(val_analog)


    def Fahrparcours_5(self):
        """
            Fahrparcours 5 ‑ Linienverfolgung : Folgen einer etwas 1,5 bis 2 cm breiten Linie auf
            dem Boden. Das Auto soll stoppen, sobald das Auto das Ende der Linie erreicht hat. Als
            Test soll eine Linie genutzt werden, die sowohl eine Rechts‑ als auch eine Linkskurve
            macht. Die Kurvenradien sollen deutlich größer sein als der maximale Radius, den das
            Auto ohne ausgleichende Fahrmanöver fahren kann.
            Zusätzlich: Hindernis-Erkennung & Stop des Fahrzeugs
        """
        count_sum_sens_0 = 0 # Zaehler für "Kein IR-Sensor findet die Spur" vorbelegen
        dist_radar = self.us.distance()

        while dist_radar > 5 or dist_radar < 0:
            # Kein Hindernis (> 5 cm), Fehler (< 0) werden ignoriert
            print(count_sum_sens_0)
            print(dist_radar)
            if self.bg_line == "0":
                sens_werte = self.ir.read_digital()
            elif self.bg_line == "1":
                sens_werte = self.invert_digital_val(self.ir.read_digital())  
            # print(sens_werte)
            # print(sum(sens_werte))
            if sum(sens_werte) != 0:
                # IR-Sensorsignale auf Intervall [-1, +1] normieren mit Div. durch "Quersumme" aller Werte
                self.lenkw_norm = ((sens_werte[0]*(-1.0) + 
                                    sens_werte[1]*(-0.5) + 
                                    sens_werte[2]*( 0.0) + 
                                    sens_werte[3]*(+0.5) + 
                                    sens_werte[4]*(+1.0) ) 
                                    / sum(sens_werte))
                count_sum_sens_0 = 0
            else:
                # Alle IR-Sensoren sind 0
                print("Spur verloren")
                count_sum_sens_0 += 1
                if count_sum_sens_0 > 5:
                    break
            # print(lenkw_norm)

            lenkwinkel = self.lenkw_norm * self.lenkw_max + 90 # Lenkwinkel fuer Servo umrechnen auf [45...135]

            self.drive(70, 1, lenkwinkel)   # Vorwaerts fahren 
            # time.sleep(0.02)                # fuer diese Zeit in s
            dist_radar = self.us.distance() # Hindernis mit US-Sensoren ermitteln, Sprung zum while-Schleifen-Anfang

        print(dist_radar)
        self.stop()  
    
    def Fahrparcours_6(self):
        """
            Fahrparcours 6 ‑ Erweiterte Linienverfolgung: Folgen eine Linie, die sowohl eine
            Rechts‑ als auch eine Linkskurve macht mit Kurvenradien kleiner als der maximale
            Lenkwinkel.
            Stoppen (evtl. schon passiert), gegenlenken, zuruecksetzen, gegenlenken, weiterfahren
        """
        while True:
            self.Fahrparcours_5()   # Ausgang aus FP_5 mit Abbruch "Spur verloren" oder "Hindernis"
            # Gegenlenken mit max. Einschlag in Gegenrichtung, Lenkwinkel fuer Servo umrechnen auf [45...135]
            if self.lenkw_norm > 0:
                lenkwinkel = self.lenkw_max * (-1) + 90
            else:
                lenkwinkel = self.lenkw_max * (+1) + 90
            self.drive(50, -1, lenkwinkel) # Zuruecksetzen
            time.sleep(0.6) # Wieder Gegenlenken in vorherige Richtung fehlt noch.
            self.stop()

            # Stoppen von Hand mit kleinem Abstand vor US-Sensoren
            dist_radar = self.us.distance()
            if dist_radar < 2 and dist_radar > 0:
                # Verlaesst die Dauerschleife mit dem FP_5-Aufruf, macht aber noch irgendetwas mit der Lenkung...
                break


def main():
    irCar = SensorCar()
    irCar.test_sensoren()
    # irCar.Fahrparcours_5()
    irCar.Fahrparcours_6()
    
    
if __name__ == "__main__":
    main()
