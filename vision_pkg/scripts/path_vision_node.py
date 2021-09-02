#!/usr/bin/python
import cv2
import numpy
try:
    import rospy
    from std_msgs.msg import Float32, Bool
    ROS_FOUND = True
except ImportError:
    print("Unable to import ROS libraries, starting script as non-node")
    ROS_FOUND = False
from math import acos, sqrt, pi

GUI_ACTIVATED = True
VISION_ACTIVATED = False
object_area = 0
h_low = 0
h_high = 179
s_low = 0
s_high = 35
v_low = 0
v_high = 255
kernel_9x9 = numpy.ones((9,9),numpy.uint8)
kernel_3x3 = numpy.ones((3,3), numpy.uint8)
lines_class1 = []
lines_class2 = []
camera_matrix = numpy.array([[]])
start_data_acq = False
accumulator = 0

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
    # create trackbars for color change
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

def classifyLines(slope, intercept):
    global lines_class1,lines_class2
    if(slope<0):
        lines_class1.append((slope,intercept))
    else:
        lines_class2.append((slope,intercept))

def get_line_equation(x1, y1,x2, y2 ):
    # receives a vector of [x1, y1, x2, y2] and returns a slope, intercept
    x = [x1, x2]
    y = [y1, y2]
    slope, intercept = numpy.polyfit(x, y, deg=1)
    return slope, intercept

def segmented_ROI(thresholded_img, cnt):
    """
    This function consists on eliminating any remaining noise around the desired object. The approach 
    consists on finding the contour with the largest area and eliminate the remaining ones. The detected
    object with the largest area is then copied and pasted in a black image. The result is a black
    and white image, similar to a binary image. This is used as the the thresholded image to be analyzed.
    """
    if(len(cnt)==0):
        return thresholded_img
    cnt = max(cnt, key=cv2.contourArea) #Find largest contour by area
    
    #Create Black image with same dimmensions of the original image
    blk_img = numpy.zeros(thresholded_img.shape, dtype = "uint8") 

    blk_img = cv2.drawContours(blk_img,[cnt],0,[255,255,0],-1) #Draw contours to avoid errors in corners
    return blk_img

def calculate_angle(x1,y1,x2,y2):
    y_difference = abs(y1-y2)
    x_difference = abs(x1-x2)
    denominator = sqrt((x_difference**2)+y_difference**2)
    angle = acos(y_difference/denominator)
    return numpy.rad2deg(angle)

def data_acq_callback(reset):
    global accumulator
    if reset.data:
        accumulator = 0

def update_accumulator_exponential_filter(new_value, weight):
    global accumulator
    if accumulator == 0:
        accumulator = new_value
    else:
        accumulator = weight*new_value + (1-weight)*accumulator

def activate_vision_callback(msg):
    global VISION_ACTIVATED
    VISION_ACTIVATED = msg.data

if ROS_FOUND:
    rospy.init_node("PathVisionNode")
    pub = rospy.Publisher("VisionAngle", Float32, queue_size = 10)
    rospy.Subscriber("VisionPathResetData", Bool, data_acq_callback)
    rospy.Subscriber("ActivatePathVision", Bool, activate_vision_callback)


while not VISION_ACTIVATED:
    continue

if GUI_ACTIVATED:
    createWindows(windows)
    createTrackbars('Thresholded')

#newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h))
cap = cv2.VideoCapture(0)
while(VISION_ACTIVATED):
    ret, img = cap.read()
    if not ret:
        continue
    #img = cv2.undistort(img, mtx, dist, None, newcameramtx)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (h_low, s_low, v_low), (h_high, s_high,v_high))
    print(mask)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_9x9) #Erosion followed by dilation
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_9x9) #Dilation follwed by erosion
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_9x9)
    _,contours,_ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnt = None
    object_area = 0
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea) #filter objects by area, get object with largest area
        object_area = cv2.contourArea(cnt)
    if object_area > 1000:
        mask = segmented_ROI(mask, contours)
        
    cannyIMG = cv2.Canny(mask,100,200)
    cannyIMG = cv2.dilate(cannyIMG, kernel_3x3, iterations = 2)

    strong_lines = numpy.zeros([4,1,2])
    
    lines = cv2.HoughLines(cannyIMG,1,numpy.pi/180,80, 20)
    line_x = []
    line_y = []
    if lines is not None:
        for line in lines:
            for rho, theta in line:
                a = numpy.cos(theta)
                b = numpy.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                if (x2 - x1) !=0:
                    slope, intercept = get_line_equation(x1,y1,x2,y2)
                    if slope > 0:
                        line_x.extend([x1,x2])
                        line_y.extend([y1,y2])
    min_y = 0
    max_y = img.shape[0]
    if len(line_x) !=0:
        poly_line = numpy.poly1d(numpy.polyfit(line_y,line_x,deg=1))
        line_start_x = int(poly_line(min_y))
        line_end_x = int(poly_line(max_y))
        start_point = (line_start_x,min_y)
        end_point = (line_end_x,max_y)
        cv2.line(img, start_point, end_point, (0,0,255), 2)
        start_point = (line_start_x,min_y,1)
        end_point = (line_end_x,max_y,1)
        #start_point = numpy.dot(newcameramtx,start_point)
        #end_point = numpy.dot(newcameramtx,end_point)
        custom_coordSys_center = (line_start_x + int(abs(line_start_x-line_end_x)/2),int(max_y/2))
        #custom_coordSys_center = (start_point[0] + int(abs(start_point[0]-end_point[0])/2),int(end_point[1]/2),1)
        custom_coordSys_point1_x = start_point[0] - custom_coordSys_center[0]
        custom_coordSys_point1_y = custom_coordSys_center[1] - start_point[1]
        custom_coordSys_point2_x = end_point[0] - custom_coordSys_center[0]
        custom_coordSys_point2_y = custom_coordSys_center[1] - end_point[1]
        angle = calculate_angle(custom_coordSys_point1_x,custom_coordSys_point1_y,custom_coordSys_point2_x,custom_coordSys_point2_y)
        update_accumulator_exponential_filter(angle, 0.10)
        if ROS_FOUND:
            rospy.loginfo(angle)
            pub.publish(accumulator)
        cv2.circle(img, custom_coordSys_center,10,(0,0,0))
    
    if GUI_ACTIVATED:
        cv2.imshow('Original', img)
        cv2.imshow('Thresholded', mask)
        cv2.waitKey(1)

cv2.destroyAllWindows()
cap.release()
rospy.spin()

