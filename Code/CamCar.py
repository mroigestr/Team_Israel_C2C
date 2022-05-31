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

    def __init__(self):
        self.bc = bc.BaseCar()
        self.Cam = bk_cam.Camera()
        self.steeringangle_dq = col.deque([0, 0]) # , 0, 0])#, 0, 0, 0, 0, 0, 0])
        self.h = 0
        self.w = 0
        self.lenkwinkel = 90
        self.hMin = self.sMin = self.vMin = 0
        self.hMax = self.sMax = self.vMax = 255
        self.ROI_left = self.ROI_right = self.ROI_bottom = self.ROI_top = 0
        self.csvDictread_HSV("calibration_hsv.csv")
        self.csvDictread_ROI("calibration_ROI.csv")
        self.timestamp_id = datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-6]
        self.image_id = 0
        self.linesfound = False
        if not os.path.exists(os.path.join(os.getcwd(), "images_FP7")):
            os.makedirs(os.path.join(os.getcwd(), "images_FP7"))
        # print(self.timestamp_id)
        # print("Init abgeschlossen")

    def csvDictread_HSV(self, source):
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
        with open(source, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.ROI_left = int(row["Left"])
                self.ROI_right = int(row["Right"])
                self.ROI_bottom = int(row["Bottom"])
                self.ROI_top = int(row["Top"])


    def video_capture(self):
        
        
        # Abfrage eines Frames            
        image = self.Cam.get_frame()

        # Resizing
        # height, width, _ = image.shape
        # image = cv.resize(image,(int(width*2/3), int(height*2/3)), interpolation = cv.INTER_CUBIC)
        # BGR2HSV-Transformation
        image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        #ROI region of Interest
        h1, w1, _ = image_hsv.shape
        # print(h1, self.ROI_bottom, self.ROI_top)
        # print(w1, self.ROI_left, self.ROI_right)
        img_hsv = image_hsv[int(self.ROI_top):int(self.ROI_bottom),int(self.ROI_left):int(self.ROI_right)]
        # mid_pic_w = w1/2
        

        # Erzeugung einer Maske (Farbfilter für blau)
        lower = np.array([self.hMin, self.sMin, self.vMin])
        upper = np.array([self.hMax, self.sMax, self.vMax])
        mask = cv.inRange(img_hsv, lower, upper) # mask ist Numpy-Array

        # mask_cn = cv.Canny(img_hsv, 50, 200)
        mask_cn = cv.Canny(mask, 199, 200)
        image_hough, x3m = self.line_detectP(mask_cn)
        self.autolenkwinkel(x3m)

        # Fahrdaten (Bild & Lenkwinkel) in JPEG schreiben
        if self.linesfound == True:
            self.save_drivingdata(img_hsv)
        
        # Visualisierung des Bilds
        img = cv.cvtColor(mask_cn, cv.COLOR_GRAY2BGR)
        img = np.hstack((img_hsv, image_hough))
        
        return img
        
    

    def line_detectP(self, mask):
         # Probabilistische Hough-Transformation
        img2 = mask.copy()
        img2 = cv.cvtColor(img2, cv.COLOR_GRAY2RGB)
       
        
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 15  # in etwa Anzahl der Punkte auf der Geraden. Je geringer Min_threshold, dest mehr Geraden werden erkannt.
        minLineLength = 8    # Minimale Linienlänge
        maxLineGap = 10       # Maximale Anzahl von Lücken in der Linie

        line_segments = cv.HoughLinesP(mask, rho, angle, min_threshold, np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

        if line_segments is None:
            self.linesfound = False
            # print("HoughLinesP hat keine Linien gefunden")
            x3m = int(self.w/2)
        else:
            # Elemente stellen Punkte des Liniensegmentes dar (x1,y1,x2,y2)
            self.linesfound = True
            lh_lines = []
            rh_lines = []

            # Vertikale Mittellinie
            self.h, self.w, _ = img2.shape
            cv.line(img2, (int(self.w/2),0), (int(self.w/2),self.h), (128,128,128), 2)

            for line in line_segments:
                x1,y1,x2,y2 = line[0]
                line_act = [x1,y1,x2,y2]
                mean_x = (x1+x2)/2

                # Aufteilung der Linien in links und rechts    
                if mean_x < int(self.w/2):
                    lh_lines.append(line_act)
                    cv.line(img2, (x1,y1),(x2,y2), (0,0,128),3)
                else:
                    rh_lines.append(line_act)
                    cv.line(img2, (x1,y1),(x2,y2), (0,128,0),3)

            # Gerade mit gegebenen Punkten (x1, y1), (x2, y2)
            # Gesucht ist der Punkt (x3, y3), gegeben ist y3
            y3 = 0 # Schnittpunkt mit der x-Achse: Oberer Bildrand

            # Durchschnitt der linken Linien 
            if len(lh_lines) == 0:
                # print("Keine Linien in der linken Bildhälfte gefunden")
                x3l = 0  # Volle Unterstützung dieser Seite
            else:
                lh_lines_mean = np.mean(lh_lines, axis=0).astype("int")
                x1,y1,x2,y2 = lh_lines_mean

                # Sehr kleinen Nenner abfangen
                dy12 = diff_epsi((y2-y1), 1e-6)
                # print("dy12:", dy12)

                # Schnittpunkt der linken "Mittellinie" mit oberem Bildrand
                x3l = int((x2-x1)/(dy12) * (y3-y1) + x1)

                cv.line(img2, (x1, y1),(x2,y2) ,(0,0,192),4)   # Gemittelte Linie links
                cv.line(img2, (x3l,y3),(x2,y2) ,(0,0,255),2)  # ... verlängert zum oberen Bildrand

            # Durchschnitt der rechten Linien 
            if len(rh_lines) == 0:
                # print("Keine Linien in der rechten Bildhälfte gefunden")
                x3r = self.w  # Volle Unterstützung dieser Seite
            else:
                rh_lines_mean = np.mean(rh_lines, axis=0).astype("int")
                x1,y1,x2,y2 = rh_lines_mean

                # Sehr kleinen Nenner abfangen
                dy12 = diff_epsi((y2-y1), 1e-6)

                # Schnittpunkt der rechten "Mittellinie" mit oberem Bildrand
                x3r = int((x2-x1)/(dy12) * (y3-y1) + x1)
                
                # print(rh_lines)
                cv.line(img2, (x1, y1),(x2,y2), (0,192,0),4)  # Gemittelte Linie rechts
                cv.line(img2, (x3r,y3),(x2,y2), (0,255,0),2)  # ... verlängert zum oberen Bildrand
 
            # Mittelpunkt der Schnittpunkte mit oberem Bildrand
            x3m = int((x3r+x3l)/2)
            # Ziellinie von unterer Bildmitte zu x3m
            cv.line(img2, (x3m,0),(int(self.w/2),self.h), (192,0,32),6)

        return img2, x3m


    def save_drivingdata(self, image):
        """
        Speichert das aktuelle Bild mit entsprechendem Lenkwinkel in Ordner als jpeg ab
        """
        jpeg = self.Cam.get_jpeg(image)
        name = f"{self.timestamp_id}_{self.image_id:03d}_{int(self.lenkwinkel):03d}.jpeg"
        print("Name", name)
        print("Typ",type(name))
        self.Cam.save_frame(
            "images_FP7/",name , image)
        self.image_id += 1


    def autolenkwinkel(self, x3m):
        
        steering_angle=np.arctan((self.w/2-x3m)/self.h)*(-1)*(180)/np.pi
        # print(steering_angle)
        
        self.steeringangle_dq.append(steering_angle)
        self.steeringangle_dq.popleft()
        self.steeringangle_m=np.mean(self.steeringangle_dq)
        self.lenkwinkel = int(self.steeringangle_m + 90)
        
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

# def save_drivingdata(self, image):
#     """
#     Speichert das aktuelle Bild mit entsprechendem Lenkwinkel in Ordner als jpeg ab
#     """
#     jpeg = self.Cam.get_jpeg(image)
#     name = f"{self.timestamp_id}_{self.image_id:03d}_{int(self.lenkwinkel):03d}.jpeg"
#     print("Name", name)
#     print("Typ",type(name))
#     self.Cam.save_frame(
#         "images_FP7/",name , image)
#     self.image_id += 1
    

def diff_epsi(diff, epsilon):
    ''' Falls |diff| < epsilon => |diff| = epsilon mit richtigem Vorzeichen '''
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