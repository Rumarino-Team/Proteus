#!/usr/bin/python
import rospy
from std_msgs.msg import Float32
from controller_pkg.msg import ControllerSetup

class AUV_Depth_Controller_Interface:

    def __init__(self):
        self._depth_controller_setup_pub = rospy.Publisher('depth_controller_setup', ControllerSetup, queue_size=10)
        self._depth_controller_pub = rospy.Publisher('depth_input', Float32, queue_size=10)

    def turn_on_controller(self, depth_polarity):
        message = ControllerSetup()
        message.changePolarity = depth_polarity
        message.controllerRunning = True
        self._depth_controller_setup_pub.publish(message)
    
    def turn_off_controller(self):
        message = ControllerSetup()
        message.controllerRunning = False
        self._depth_controller_setup_pub.publish(message)

    def go_to_depth(self, depth_in_feet):
        self._depth_controller_pub.publish(float(depth_in_feet))