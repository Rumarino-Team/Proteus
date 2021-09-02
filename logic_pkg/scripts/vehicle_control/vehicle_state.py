#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
class AUV_State:

    def __init__(self):
        self.is_moving_forwards = False
        self.is_moving_down = False
        self.is_absolute_heading = False
        self.current_angle = 0
        self.current_depth = 0
        rospy.Subscriber("depth_current", Float32, self.depth_current_callback)
        rospy.Subscriber("yaw_current", Float32, self.yaw_current_callback)

    def depth_current_callback(self, depth_message):
        self.current_depth = depth_message.data
    
    def yaw_current_callback(self, yaw_message):
        self.current_angle = yaw_message.data