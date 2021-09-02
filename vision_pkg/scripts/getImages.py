#!/usr/bin/python
import numpy as np
import cv2
import rospy
from std_msgs.msg import Float32
import time

cap = cv2.VideoCapture(0)
x1=1
angle = 0
def anglecurr(x):
    global angle	
    angle = x.data
rospy.init_node("CaptureImage")
rospy.Subscriber("yaw_current",Float32, anglecurr)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    filename = 'image' +  str(int(x1)) + ".jpg"
    x1+=1
    ange = str(angle)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,ange,(10,20),font, 1,(0,0,0),2,cv2.LINE_AA)
    cv2.imwrite(filename, frame)
    #cv2.imshow("imag",frame)
    time.sleep(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
