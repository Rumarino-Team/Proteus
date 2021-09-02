#!/usr/bin/env python

"""
#The differential controller script is responsible sending velocity commands
#to the Arduino that controls de DC Motors. Here the Twist message coming from 
#the teleop device is converted into MotorCommand message used by the Arduino.
"""

import rospy
from controller_pkg.msg import HorizontalMotors
from geometry_msgs.msg import Twist

# Motor global variables 
global dict
dict = {'MOTOR_CAP': 30}

# Converts incoming Twist message to Motorommand message and
# sends the command to the Arduino.
def diff_control_callback(twistData):
  command = HorizontalMotors()
  command.leftMotor = int((twistData.linear.x + twistData.angular.z) * dict['MOTOR_CAP'])
  command.rightMotor = int((twistData.linear.x - twistData.angular.z) * dict['MOTOR_CAP'])

  pub.publish(command)

# Main function, waits for new Twist messages to arrive
# Creates node and subscriber
def diff_controller_listener():
  global pub
  rospy.init_node('joystick_controller')
  rospy.Subscriber('cmd_vel', Twist, diff_control_callback)
  pub = rospy.Publisher('horizontal_motors', HorizontalMotors, queue_size = 10)

  rospy.spin()

if __name__ == '__main__':
    diff_controller_listener()



