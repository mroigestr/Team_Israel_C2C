import cv2
import sys
import numpy as np
import basisklassen_cam as bkc
import csv

def hsv_helper(img):
    def nothing(x):
        pass
    # Create a window
    window_id='Press q to quit'
    cv2.namedWindow(window_id)
    # create trackbars for color change
    cv2.createTrackbar('HMin',window_id,0,255,nothing) # Hue is from 0-179 for Opencv
    cv2.createTrackbar('HMax',window_id,0,255,nothing)
    cv2.createTrackbar('SMin',window_id,0,255,nothing)
    cv2.createTrackbar('SMax',window_id,0,255,nothing)
    cv2.createTrackbar('VMin',window_id,0,255,nothing)
    cv2.createTrackbar('VMax',window_id,0,255,nothing)
    
    
    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', window_id, 255)
    cv2.setTrackbarPos('SMax', window_id, 255)
    cv2.setTrackbarPos('VMax', window_id, 255)
    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    output = img
    while(1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin',window_id)
        sMin = cv2.getTrackbarPos('SMin',window_id)
        vMin = cv2.getTrackbarPos('VMin',window_id)
        hMax = cv2.getTrackbarPos('HMax',window_id)
        sMax = cv2.getTrackbarPos('SMax',window_id)
        vMax = cv2.getTrackbarPos('VMax',window_id)
        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)
        cv2.imshow(window_id,output)
        if cv2.waitKey(30) == ord('q'):
            break
    # calibration_dict = {"hMin": hMin, "sMin": sMin, "vMin": vMin, "hMax": hMax, "sMax": sMax, "vMax": vMax}
    write2csv(hMin, sMin, vMin, hMax, sMax, vMax)
    cv2.destroyAllWindows()

def write2csv(hMin, sMin, vMin, hMax, sMax, vMax):

    header = ['hMin', 'sMin', 'vMin', 'hMax', 'sMax', 'vMax']
    data = [hMin, sMin, vMin, hMax, sMax, vMax]

    with open('calibration_hsv.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(data)


c = bkc.Camera()
img = c.get_frame()
c.release()
hsv_helper(img)
