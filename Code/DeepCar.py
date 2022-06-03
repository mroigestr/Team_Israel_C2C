import basisklassen_cam as bk_cam
import BaseCar as bc
import cv2 as cv
# import matplotlib.pyplot as plt
import numpy as np
# import collections as col
import csv
# from datetime import datetime
# import os.path
import collections as col
# from typing import List
import os
# import datetime
#import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
#from tensorflow.keras.layers import Normalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv2D, Dropout, Flatten


class DeepCar(object):

    def __init__(self):
        self.model = load_model('JohnyCar_PH.h5')
        self.bc = bc.BaseCar()
        self.Cam = bk_cam.Camera()
        self.ROI_left = self.ROI_right = self.ROI_bottom = self.ROI_top = 0
        self.csvDictread_ROI("calibration_ROI.csv")
        print("Init abgeschlossen")



    def csvDictread_ROI(self, source):
        with open(source, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.ROI_left = int(row["Left"])
                self.ROI_right = int(row["Right"])
                self.ROI_bottom = int(row["Bottom"])
                self.ROI_top = int(row["Top"])


    def video_capture(self):
        """
        Methode zur Bild-Erzeugung, Reduktion auf relevanten Bildbereich & Konvertierung in den HSV-Farbraum
        Input: kein Input erforderlich
        Output: 
            - img_hsv: Bild im HSV-Farbraum zur Ausgabe
            - img_list: Bild in Liste zur Verwendung für neuronales Netz
        """
        
        
        # Abfrage eines Frames            
        image = self.Cam.get_frame()

        image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        #ROI region of Interest
        img_hsv = image_hsv[int(self.ROI_top):int(self.ROI_bottom),int(self.ROI_left):int(self.ROI_right)]
        
        # resize Numpy-Array
        list = [img_hsv]
        img_list = np.array(list)
        
        return img_hsv, img_list

    def Fahrpacours_8(self):
        """
        Fahrspurverfolgung mittels eines Neuronalen Netzes.
        -> Einlesen der Bilder; Ausgabe des Lenkwinkels mit Hilfe des neuronalen Netzes
        Input: kein Input
        Output: kein Output
        """
        while True:
            # Bild-Erzeugung
            img, img_list = self.video_capture()
            # Berechnung Lenkwinkel
            lw_predict = self.model.predict(img_list)
            # Darstellung des Bilds
            cv.imshow("Display window (press q to quit)", img)
            # Ende bei Drücken der Taste q
            if cv.waitKey(1) == ord('q'):
                break
            # Fahrbefehl mit berechnetem Lenkwinkel
            self.bc.drive(30, 1, lw_predict)
        
        self.bc.stop()
        self.Cam.release()



def main():
    cnn_Car = DeepCar()
    cnn_Car.Fahrpacours_8()
    
if __name__ == '__main__':
    main()