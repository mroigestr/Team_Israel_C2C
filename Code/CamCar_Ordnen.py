import basisklassen_cam as bk_cam
import BaseCar as bc
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import collections as col
import csv
from datetime import datetime
import os.path


class CamCar(object):
    """ Steuerung des PiCar via Kamera 
    """
    def __init__(self):
        self.bc = bc.BaseCar()
        self.Cam = bk_cam.Camera()
        self.steeringangle_dq = col.deque([0, 0]) # Sammeln von Lenkwinkeln [Anzahl Einträge] zur Beruhigung der Ausgabe
        self.h = 0
        self.w = 0
        self.lenkwinkel = 90
        # Vorbelegen der Kameraparameter: HSV-Farbraum, Region Of Interest (ROI)
        self.hMin = self.sMin = self.vMin = 0
        self.hMax = self.sMax = self.vMax = 255
        self.ROI_left = self.ROI_right = self.ROI_bottom = self.ROI_top = 0
        self.csvDictread_HSV("calibration_hsv.csv")
        self.csvDictread_ROI("calibration_ROI.csv")
        self.linesfound = False # Wert aus Methode "line_detectP", ob Linien gefunden wurden
        # Dateinamen der Bilder erzeugen
        self.timestamp_id = datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-6] # Zeitstempel nur zum Anfang des Programmstands
        # print(self.timestamp_id)
        self.image_id = 0 # Fortlaufende Bildnummer nach dem Zeitstempel
        if not os.path.exists(os.path.join(os.getcwd(), "images_FP7")):
            os.makedirs(os.path.join(os.getcwd(), "images_FP7"))
        # print("Init abgeschlossen")


    def csvDictread_HSV(self, source):
        """ HSV-Farbraum-Parameter laden 
        """
        with open(source, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.hMin = int(row["hMin"])
                self.sMin = int(row["sMin"])
                self.vMin = int(row["vMin"])
                self.hMax = int(row["hMax"])
                self.sMax = int(row["sMax"])
                self.vMax = int(row["vMax"])


    def csvDictread_ROI(self, source):
        """ Region Of Interest innerhalb des Kamerabildes laden 
            Vertikaler Bereich mit Seitenmarkierungen ohne Störkonturen
            Horizontaler Bereich evtl. auch eingrenzen
            Null-Punkt [0,0] ist links oben!
        """
        with open(source, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.ROI_left = int(row["Left"])
                self.ROI_right = int(row["Right"])
                self.ROI_bottom = int(row["Bottom"])
                self.ROI_top = int(row["Top"])


    def video_capture(self):
        """ Kamera aktivieren und Bild analysieren 
        """
        # Abfrage eines Frames            
        image = self.Cam.get_frame()

        # Resizing - Zugunsten ROI deaktiviert
        # height, width, _ = image.shape
        # image = cv.resize(image,(int(width*2/3), int(height*2/3)), interpolation = cv.INTER_CUBIC)

        # cv arbeitet nativ im BGR-Farbraum: Transformation in den HSV-Farbraum, um eine Farbe über "H" explizit einzugrenzen
        image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        # ROI Region of Interest: Bild auf linienrelevanten Bereich zuschneiden
        h1, w1, _ = image_hsv.shape
        # print(h1, self.ROI_bottom, self.ROI_top)
        # print(w1, self.ROI_left, self.ROI_right)
        img_hsv = image_hsv[int(self.ROI_top):int(self.ROI_bottom),int(self.ROI_left):int(self.ROI_right)]

        # Erzeugung einer Maske (Farbfilter für Blau)
        lower = np.array([self.hMin, self.sMin, self.vMin]) # Untere Grenze aus Vorbelegung
        upper = np.array([self.hMax, self.sMax, self.vMax]) # Obere Grenze aus Vorbelegung
        mask = cv.inRange(img_hsv, lower, upper) # mask ist Numpy-Array

        # Canny-Edge-Detection erkennt Kanten mit Kontrast (minVal, maxVal) => Schwarz/Weiß-Bild
        mask_cn = cv.Canny(mask, 199, 200) 

        # Ermittelt Linien aus Seitenmarkierungen und gibt Zielpunkt am oberen Bildrand zurück
        image_hough, x3m = self.line_detectP(mask_cn)

        # Ermittelt Lenkwinkel aus dem Zielpunkt am oberen Bildrand in PiCar-Koordinaten [45° ... 135°]
        self.autolenkwinkel(x3m)

        # Fahrdaten (Bild & Lenkwinkel) in JPEG schreiben
        if self.linesfound == True:
            self.save_drivingdata(img_hsv)
        
        # Visualisierung des Bilds
        img = cv.cvtColor(mask_cn, cv.COLOR_GRAY2BGR)
        img = np.hstack((img_hsv, image_hough))
        
        return img


    def line_detectP(self, mask):
        """ Probabilistische Hough-Transformation 
        """
        img2 = mask.copy()
        img2 = cv.cvtColor(img2, cv.COLOR_GRAY2RGB)

        # Parameter für HoughLinesP
        rho = 1              # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 15   # in etwa Anzahl der Punkte auf der Geraden. Je geringer min_threshold, desto mehr Geraden werden erkannt.
        minLineLength = 8    # Minimale Linienlänge
        maxLineGap =    10   # Maximale Anzahl von Lücken in der Linie

        line_segments = cv.HoughLinesP(mask, rho, angle, min_threshold, np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

        if line_segments is None:
            # print("HoughLinesP hat keine Linien gefunden")
            self.linesfound = False
            x3m = int(self.w/2) # Zielpunkt am oberen Bildrand mittig vorbelegen
        else:
            # Elemente stellen Punkte des Liniensegmentes dar (x1,y1, x2,y2)
            self.linesfound = True
            lh_lines = [] # Linke Linien leer vorbelegen
            rh_lines = [] # Rechte Linien leer vorbelegen

            # Vertikale Mittellinie
            self.h, self.w, _ = img2.shape
            cv.line(img2, (int(self.w/2),0), (int(self.w/2),self.h), (128,128,128), 2)

            for line in line_segments:
                x1,y1, x2,y2 = line[0]
                line_act = [x1,y1, x2,y2]
                # Unterscheidungsmerkmal einer Linie für links oder rechts
                x_mean = (x1+x2)/2
                # x_mean = x1

                # Aufteilung der Linien in links und rechts    
                if x_mean < int(self.w/2):
                    lh_lines.append(line_act) # Linke Linie anhängen
                    cv.line(img2, (x1,y1),(x2,y2), (0,0,128),3) # Linke Linie einzeichnen
                else:
                    rh_lines.append(line_act) # Rechte Linie anhängen
                    cv.line(img2, (x1,y1),(x2,y2), (0,128,0),3) # Rechte Linie einzeichnen

            # Gerade mit gegebenen Punkten (x1,y1), (x2,y2)
            # Gesucht ist der Punkt (x3,y3), gegeben ist y3
            y3 = 0 # Schnittpunkt mit der x-Achse: Oberer Bildrand

            # Durchschnitt der linken Linien 
            if len(lh_lines) == 0:
                # print("Keine Linien im linken Bildbereich gefunden")
                x3l = 0  # Volle Unterstützung dieser Seite
            else:
                # Mittelwert aller linken Linien
                lh_lines_mean = np.mean(lh_lines, axis=0).astype("int")
                x1,y1, x2,y2 = lh_lines_mean # "Mittellinie" links entpacken

                # Linien mit ihrer Länge gewichten
                x1,y1, x2,y2 = line_weight(lh_lines)

                # Sehr kleinen Nenner abfangen
                dy12 = diff_epsi((y2-y1), 1)

                # Schnittpunkt der linken "Mittellinie" mit oberem Bildrand
                x3l = int((x2-x1)/(dy12) * (y3-y1) + x1)

                cv.line(img2, (x1, y1),(x2,y2) ,(0,0,192),4)   # "Mittellinie" links einzeichnen
                cv.line(img2, (x3l,y3),(x2,y2) ,(0,0,255),2)   # ... verlängert zum oberen Bildrand

            # Durchschnitt der rechten Linien 
            if len(rh_lines) == 0:
                # print("Keine Linien im rechten Bildbereich gefunden")
                x3r = self.w  # Volle Unterstützung dieser Seite
            else:
                # Mittelwert aller rechten  Linien
                rh_lines_mean = np.mean(rh_lines, axis=0).astype("int")
                x1,y1,x2,y2 = rh_lines_mean # "Mittellinie" rechts entpacken

                # Linien mit ihrer Länge gewichten
                x1,y1, x2,y2 = line_weight(rh_lines)

                # Sehr kleinen Nenner abfangen
                dy12 = diff_epsi((y2-y1), 1)

                # Schnittpunkt der rechten "Mittellinie" mit oberem Bildrand
                x3r = int((x2-x1)/(dy12) * (y3-y1) + x1)
                
                # print(rh_lines)
                cv.line(img2, (x1, y1),(x2,y2), (0,192,0),4)   # "Mittellinie" rechts einzeichnen
                cv.line(img2, (x3r,y3),(x2,y2), (0,255,0),2)   # ... verlängert zum oberen Bildrand
 
            # Mittelpunkt der Schnittpunkte der "Mittellinien" mit oberem Bildrand
            x3m = int((x3r+x3l)/2)
            # Ziellinie von unterer Bildmitte zu x3m einzeichnen
            cv.line(img2, (x3m,0),(int(self.w/2),self.h), (192,0,32),6)

        return img2, x3m


    def save_drivingdata(self, image):
        """ Speichert das aktuelle Bild mit entsprechendem Lenkwinkel in Ordner als jpeg ab
        """
        jpeg = self.Cam.get_jpeg(image)
        name = f"{self.timestamp_id}_{self.image_id:03d}_{int(self.lenkwinkel):03d}.jpeg"
        print("jpeg-Name:", name)
        self.Cam.save_frame("images_FP7/", name, image)
        self.image_id += 1 # Image-ID hochzählen


    def autolenkwinkel(self, x3m):
        """ Ermittelt Lenkwinkel aus dem Zielpunkt am oberen Bildrand in PiCar-Koordinaten [45° ... 135°]
        """
        steering_angle = np.arctan((self.w/2-x3m)/self.h)*(-1)*(180)/np.pi
        # print(steering_angle)

        # Sammeln von Lenkwinkeln [Anzahl Einträge in init] zur Beruhigung der Ausgabe        
        self.steeringangle_dq.append(steering_angle)
        self.steeringangle_dq.popleft() # Rechts neu, links fallen lassen
        self.steeringangle_m = np.mean(self.steeringangle_dq)
        self.lenkwinkel = int(self.steeringangle_m + 90)
        # Eingrenzen der Lenkwinkel auf Intervall [45° ... 135°] zur direkten PiCar-Ansteuerung
        if self.lenkwinkel < 45:
            self.lenkwinkel = 45
        elif self.lenkwinkel > 135:
            self.lenkwinkel = 135
              

    def Fahrparcours_7(self):
        while True:
            img = self.video_capture()
            cv.imshow("Display window (press q to quit)", img)
            # Ende bei Drücken der Taste q
            if cv.waitKey(1) == ord('q'):
                break
            self.bc.drive(30, 1, self.lenkwinkel)
            
        self.bc.stop()
        self.Cam.release()


def line_weight(lines):
    """ Mittlere Linie aller Linien mit deren Länge gewichten 
    """
    line_len_sum = 0
    x1_sum = y1_sum = x2_sum = y2_sum = 0
    for line in lines:
        x1,y1, x2,y2 = line # Liste der Linie entpacken
        line_len = np.sqrt((x2-x1)**2 + (y2-y1)**2) # Länge der Linie mit Pythagoras
        line_len_sum += line_len # Summe der Linienlängen
        # Koordinaten mit Linienlänge gewichten
        x1_sum += x1*line_len
        y1_sum += y1*line_len
        x2_sum += x2*line_len
        y2_sum += y2*line_len
    # Koordinaten mit Summe der Linienlängen "normieren"
    x1 = int(x1_sum/line_len_sum)
    y1 = int(y1_sum/line_len_sum)
    x2 = int(x2_sum/line_len_sum)
    y2 = int(y2_sum/line_len_sum)
    return x1,y1, x2,y2


def diff_epsi(diff, epsilon):
    """ Falls |diff| < epsilon => |diff| = epsilon mit richtigem Vorzeichen 
    """
    if abs(diff) < epsilon:
        if diff >= 0:
            diff = epsilon
        else:
            diff = -epsilon
    return diff


def main():
    TestCam = CamCar()
    TestCam.Fahrparcours_7()


if __name__ == '__main__':
    main()
