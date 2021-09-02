#!/usr/bin/python

import cv2
import numpy as np
try:
    import rospy
    from std_msgs.msg import Float32, Bool, Int32
    ROS_FOUND = True
except ImportError:
    print("Unable to import ROS libraries, starting script as non-node")
    ROS_FOUND = False

h_low = 92
h_high = 126
s_low = 85
s_high = 219
v_low = 62
v_high = 161

windows = ['Original', 'Thresholded']

def getTrackbarsPositions(x):
    global h_low, h_high
    if(x>=h_high):
        h_low = h_high
    else:
        h_low = x

def getTrackbarsPositions1(x):
    global h_high
    h_high = x

def getTrackbarsPositions2(x):
    global s_low, s_high
    if(x>=s_high):
        s_low = s_high
    else:
        s_low = x

def getTrackbarsPositions3(x):
    global s_high
    s_high = x

def getTrackbarsPositions4(x):
    global v_low, v_high
    if(v_low>=v_high):
        v_low = v_high
    else:
        v_low = x

def getTrackbarsPositions5(x):
    global v_high
    v_high = x

def createTrackbars(windowName):
    global h_low, h_high, s_low, s_high, v_low, v_high
    cv2.createTrackbar('H Low',windowName,0,179,getTrackbarsPositions)
    cv2.createTrackbar('H High',windowName,0,179,getTrackbarsPositions1)
    cv2.createTrackbar('S Low',windowName,0,255,getTrackbarsPositions2)
    cv2.createTrackbar('S High',windowName,0,255,getTrackbarsPositions3)
    cv2.createTrackbar('V Low',windowName,0,255,getTrackbarsPositions4)
    cv2.createTrackbar('V High',windowName,0,255,getTrackbarsPositions5)
    cv2.setTrackbarPos('H Low',windowName,h_low)
    cv2.setTrackbarPos('H High',windowName,h_high)
    cv2.setTrackbarPos('S Low',windowName,s_low)
    cv2.setTrackbarPos('S High',windowName,s_high)
    cv2.setTrackbarPos('V Low',windowName,v_low)
    cv2.setTrackbarPos('V High',windowName,v_high)

def createWindows(windowsNames):
    for name in windowsNames:
        cv2.namedWindow(name)









GUI_ACTIVATED = True

if GUI_ACTIVATED:
    createWindows(windows)
    createTrackbars('Thresholded')

if ROS_FOUND:
    rospy.init_node("BuoyVisionNode")
    pub = rospy.Publisher("yaw_current_vision", Int32, queue_size = 1)


cap = cv2.VideoCapture(0)
centroid = None
ret, img_original = cap.read()
_, img_width, _ = img_original.shape
img_center = int(img_width/2)
while(True):
    ret, img_original = cap.read()
    #hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#BGR to HSV-Space conversion
    if not ret:
        continue
    blurred = cv2.GaussianBlur(img_original,(11,11),0)
    img = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    #Path color parameters (yellow-green) 
    #lower_color = np.array([0,30,30], dtype = 'uint8')
    #upper_color = np.array([70,180,255], dtype = 'uint8')
    #Image Segmentation
    # Construct a mask for the desired color
    mask = cv2.inRange(img, (h_low, s_low, v_low), (h_high, s_high,v_high))

    #Morphological Functions
    # Perform a series of dilations and erosions to remove any small
    # blobs left in the mask
    #kernel = np.ones((9,9),np.uint8)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    _,cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 40:
            offset_from_center = img_center-int(x)
            print(int(offset_from_center))
            if(ROS_FOUND):
                pub.publish(int(offset_from_center))
            cv2.circle(img_original, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(img_original, center, 5, (0, 0, 255), -1)
    if GUI_ACTIVATED:
        cv2.imshow('Original', img_original)
        cv2.imshow('Thresholded', mask)
        cv2.waitKey(1)
