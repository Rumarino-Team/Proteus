#!/usr/bin/env python

"""
#The differential controller script is responsible sending velocity commands
#to the Arduino that controls de DC Motors. Here the Twist message coming from 
#the teleop device is converted into MotorCommand message used by the Arduino.
"""

import rospy
from controller_pkg.msg import HorizontalMotors, VerticalMotors, ControllerSetup
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

# Motor global variables 
global dict, controllers_activated, horizontal_motors_pub, vertical_motors_pub
global yaw_controller_pub, yaw_controller_setup_pub, depth_controller_pub, depth_controller_setup_pub
global degrees, depth
global angular_scale, linear_scale
global invert_align, invert_depth
angular_scale = 1
linear_scale = 0.5
degrees = 30.0
depth = 3.0
controllers_activated = False
invert_align = True
invert_depth = True
dict = {'MOTOR_CAP': 30}

def turn_on_controllers(turn_on_bool, invert_align, invert_depth):
  global yaw_controller_setup_pub, depth_controller_setup_pub
  message = ControllerSetup()
  message.controllerGain = -1
  message.controllerBias = -1
  message.changePolarity = invert_align
  message.controllerRunning = turn_on_bool
  yaw_controller_setup_pub.publish(message)
  message.changePolarity = invert_depth
  depth_controller_setup_pub.publish(message)

def joy_to_twist(axesData):
  twistData = Twist()
  twistData.angular.z = angular_scale*axesData[0]
  twistData.linear.x = linear_scale*axesData[1]
  return twistData

def control_callback(data):
  if joy.buttons[9]:
    controllers_activated = ~controllers_activated
  else:
    if controllers_activated:
      if joy.buttons[4]:
	yaw_controller_pub.publish(degrees)
      elif joy.buttons[5]:
	yaw_controller_pub.publish(-degrees)
      elif joy.buttons[6]:
        depth_controller_pub.publish(depth)
      elif joy.buttons[7]:
        depth_controller_pub.publish(-depth)
    twistData = joy_to_twist(data.axes)
    command = HorizontalMotors()
    command.leftMotor = int((twistData.linear.x + twistData.angular.z) * dict['MOTOR_CAP'])
    command.rightMotor = int((twistData.linear.x - twistData.angular.z) * dict['MOTOR_CAP'])
    horizontal_motors_pub.publish(command)
    command = VerticalMotors()
    command.frontRight = int( data.axes[3] * dict['MOTOR_CAP'] )
    command.frontLeft = int( data.axes[3] * dict['MOTOR_CAP'] )
    command.backRight = int( data.axes[3] * dict['MOTOR_CAP'] )
    command.backLeft = int( data.axes[3] * dict['MOTOR_CAP'] )
    vertical_motors_pub.publish(command) 

# Main function, waits for new Twist messages to arrive
# Creates node and subscriber
def controller_listener():
  global horizontal_motors_pub, vertical_motors_pub
  global yaw_controller_pub, yaw_controller_setup_pub
  global depth_controller_pub, depth_controller_setup_pub
  global invert_align, invert_depth
  rospy.init_node('joystick_controller')
  #rospy.Subscriber('cmd_vel', Twist, diff_control_callback)
  rospy.Subscriber('joy', Joy, control_callback)
  horizontal_motors_pub = rospy.Publisher('horizontal_motors', HorizontalMotors, queue_size = 10)
  vertical_motors_pub = rospy.Publisher('vertical_motors', VerticalMotors, queue_size = 10)
  yaw_controller_pub = rospy.Publisher('align_input', Float32, queue_size = 10)
  yaw_controller_setup_pub = rospy.Publisher('align_controller_setup', ControllerSetup, queue_size=10)
  depth_controller_pub = rospy.Publisher('depth_input', Float32, queue_size = 10)
  depth_controller_setup_pub = rospy.Publisher('depth_controller_setup', ControllerSetup, queue_size=10)
  rospy.sleep(2)
  turn_on_controllers(True, invert_align, invert_depth)
  rospy.spin()

if __name__ == '__main__':
    controller_listener()



