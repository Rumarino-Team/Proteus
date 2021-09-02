#!/usr/bin/python
import rospy
from std_msgs.msg import Float32
from controller_pkg.msg import ControllerSetup, ForwardsCommand

class AUV_Yaw_Controller_Interface:

    def __init__(self):
        self._yaw_controller_setup_pub = rospy.Publisher('yaw_controller_setup', ControllerSetup, queue_size=10)
        self._yaw_controller_angle_pub = rospy.Publisher('yaw_input', Float32, queue_size=10)
        self._forwards_command_pub = rospy.Publisher('forwards_command', ForwardsCommand, queue_size=10)

    def turn_on_controller(self, yaw_polarity):
        message = ControllerSetup()
        message.changePolarity = yaw_polarity
        message.controllerRunning = True
        self._yaw_controller_setup_pub.publish(message)

    def turn_off_controller(self):
        message = ControllerSetup()
        message.controllerRunning = False
        self._yaw_controller_setup_pub.publish(message)
    
    def change_angle_by(self, degrees):
        """
        Counter clockwise is positive
        """
        self._yaw_controller_angle_pub.publish(float(degrees))
    
    def set_setpoint_as_current_imu_reading(self):
        self._yaw_controller_angle_pub.publish(float(1000))

    def move_forwards_backwards(self, motor_intensity, moving_forwards):
        message = ForwardsCommand()
        message.motorIntensity = motor_intensity
        message.movingForwards = moving_forwards
        self._forwards_command_pub.publish(message)