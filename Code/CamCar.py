import basisklassen_cam as bk_cam
import BaseCar as bc
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

class CamCar(object):

    def __init__(self):
        self.Cam = bk_cam.Camera()
        print("Init abgeschlossen")

    def video_capture(self):
        

        # # Schleife für Video Capturing
        while True:
            # Abfrage eines Frames            
            image = self.Cam.get_frame()
            # Resizing
            height, width, _ = image.shape
            image = cv.resize(image,(int(width*2/3), int(height*2/3)), interpolation = cv.INTER_CUBIC)
            # BGR2HSV-Transformation
            img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            # Erzeugung einer Maske (Farbfilter für blau)
            lower = np.array([100, 0, 0])
            upper = np.array([120, 255, 255])
            mask = cv.inRange(img_hsv, lower, upper) # mask ist Numpy-Array

            # mask_cn = cv.Canny(img_hsv, 50, 200)
            mask_cn = cv.Canny(mask, 50, 100)

            image_hough = self.line_detection(mask)
            # image_hough = self.line_detectP(mask)

            # Visualisierung des Bilds
            # cv.imshow("Display window (press q to quit)", mask)
            cv.imshow("Display window (press q to quit)", image_hough)
            # Ende bei Drücken der Taste q
            if cv.waitKey(1) == ord('q'):
                break
        # Kamera-Objekt muss "released" werden, um "später" ein neues Kamera-Objekt erstellen zu können!!!
        self.Cam.release()
    
    def line_detection(self, mask):
        # Klassische Hough-Transformation
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180   # angular precision in radian, i.e. 1 degree
        min_threshold = 80  # minimal of votes, Je geringer Min_threshold, dest mehr Geraden werden erkannt.

        parameter_mask = cv.HoughLines(mask, rho, angle, min_threshold)
        print("Shape Parameter_mask:", parameter_mask.shape)
        
        img2 = mask.copy()
        img2 = cv.cvtColor(img2, cv.COLOR_GRAY2RGB)
        for line in parameter_mask:
            rho,theta = line[0]
            if abs(np.sin(theta)) < 1e-6:
                a = 1000
                b = 1000
            else:
                a = -np.cos(theta)/np.sin(theta) # Anstieg der Gerade
                b = rho/np.sin(theta)            # Absolutglied/Intercept/Schnittpunkt mit der y-Achse
            x1 = 0
            y1 = int(b)
            x2 = 1000
            y2 = int(a*1000+b)
            #print(x1,x2,y1,y2)
            img2 = cv.line(img2, (x1,y1), (x2,y2), (200,100,100), 1) # adds a line to an image
            cv.putText(img2, 
                text = 'erkannte Geraden',
                org=(10,190), # Position
                fontFace= cv.FONT_HERSHEY_SIMPLEX,
                fontScale = .8, # Font size
                color = (120,255,255), # Color in hsv
                thickness = 2)
        return img2
        

    def line_detectP(self, mask):
        # Probalistische Hough-Transformation
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 10   # in etwa Anzahl der Punkte auf der Geraden. Je geringer Min_threshold, dest mehr Geraden werden erkannt.
        minLineLength = 8    # Minimale Linienlänge
        maxLineGap = 4       # Maximale Anzahl von Lücken in der Linie

        line_segments = cv.HoughLinesP(mask, rho, angle, min_threshold, np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)
        print(line_segments.shape)
        # Elemente stellen Punkte des Liniensegmentes dar (x1,y1,x2,y2)
        line_segments[:2]


def main():
    # TestCam = bk_cam.Camera()   
    TestCam = CamCar()
    TestCam.video_capture()
    
if __name__ == '__main__':
    main()