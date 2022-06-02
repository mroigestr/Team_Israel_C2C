import basisklassen_cam as bk_cam
import BaseCar as bc
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import collections as col
import csv
from datetime import datetime
import os.path
import collections as col
from typing import List
import os
import datetime
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
        self.model = load_model('JohnyCar_PH_v1.h5')
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
                print(self.ROI_top)


    def video_capture(self):
        
        
        # Abfrage eines Frames            
        image = self.Cam.get_frame()

        image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        #ROI region of Interest
        img_hsv = image_hsv[int(self.ROI_top):int(self.ROI_bottom),int(self.ROI_left):int(self.ROI_right)]
        
        # resize Numpy-Array
        list = [img_hsv]
        img_list = np.array(list)
        # img_hsv = np.concatenate(np.array([1]), img_hsv)

        return img_hsv, img_list

    def Fahrpacours_8(self):
        while True:
            img, img_list = self.video_capture()
            lw_predict = self.model.predict(img_list)
            print("lw_predict",lw_predict)
            cv.imshow("Display window (press q to quit)", img)
            # Ende bei Drücken der Taste q
            if cv.waitKey(1) == ord('q'):
                break
        
            self.bc.drive(30, 1, lw_predict)
        
        self.bc.stop()
        self.Cam.release()



def main():
    cnn_Car = DeepCar()
    cnn_Car.Fahrpacours_8()
    
if __name__ == '__main__':
    main()