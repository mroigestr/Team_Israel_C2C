import cv2
import sys
import numpy as np
import basisklassen_cam as bkc
import csv

def shape_ROI(img):
    def nothing(x):
        pass
    
    h, w, _ = img.shape
    # Create a window
    window_id='Press q to quit'
    cv2.namedWindow(window_id)
    # create trackbars for color change
    cv2.createTrackbar('Left',window_id,0,w,nothing) # Hue is from 0-179 for Opencv
    cv2.createTrackbar('Right',window_id,0,w,nothing)
    cv2.createTrackbar('Top',window_id,0,h,nothing)
    cv2.createTrackbar('Bottom',window_id,0,h,nothing)
    
    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('Right', window_id, w)
    cv2.setTrackbarPos('Bottom', window_id, h)
    
    # Initialize to check if values changes
    left = right = bottom = top= 0
    output = img
    while(1):
        img2 = img.copy()
        # get current positions of all trackbars
        left = cv2.getTrackbarPos('Left',window_id)
        right = cv2.getTrackbarPos('Right',window_id)
        bottom = cv2.getTrackbarPos('Bottom',window_id)
        top = cv2.getTrackbarPos('Top',window_id)

        # Set values to display
        # img_ROI = img[int(bottom):int(top),int(left):int(right)]
        
        # Create lines for ROI
        cv2.line(img2, (left,bottom),(left,top), (0,128,0),3)
        cv2.line(img2, (right,bottom),(right,top), (0,128,0),3)
        cv2.line(img2, (left,bottom),(right,bottom), (0,128,0),3)
        cv2.line(img2, (left,top),(right,top), (0,128,0),3)
        cv2.imshow(window_id,img2)
        if cv2.waitKey(30) == ord('q'):
            break
    
    write2csv(left, right, bottom, top)
    cv2.destroyAllWindows()

def write2csv(left, right, bottom, top):

    header = ['Left', 'Right', 'Bottom', 'Top']
    data = [left, right, bottom, top]

    with open('calibration_ROI.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(data)




c = bkc.Camera()
img = c.get_frame()
c.release()
shape_ROI(img)
