#!/usr/bin/env python
import rospy
from controller_pkg.msg import HorizontalMotors, VerticalMotors


"""
This function is used to calculate the corresponding pwm for a thrust value.
This allows us to have the same thrust forwards and backwards. Using pwm alone
we would get more thrust for positive thrust values than for negative thrust
values.

@params: Thrust data
@output: PWM value in [1100, 1500]

"""
def thrust_to_pwm(Thrust):
    PWM = 0
    if ( Thrust == 0 ):
        PWM = 1500

    elif ( Thrust > 0 ):
        PWM = 1525.102813 + 93.159161 * Thrust - 4.9300467 * Thrust**2

    else:
        PWM = 1471.689475 + 153.2462469 * Thrust - 15.2740207 * Thrust**2

    return PWM

"""
This function scales the calculated PWM to a percent. This is the format that 
the motors can receive.

@params: PWM - value in [1100, 1900]
@output: Percent - value in [-100, 100]
"""
def pwm_to_percent(pwm):
    return (pwm-1500)/4


class Horizontal_Motors:

    def __init__(self):
        self.h_motor_publisher = rospy.Publisher('horizontal_motors', HorizontalMotors, queue_size=10)
        self.FORWARDS_CAP_PERCENT = 40
        self.ANGULAR_CAP_PERCENT = 40
        self.forwards_speed_percent = 0
        self.motor_polarity = -1
    
    def publish_to_motors_forwards(self, left_speed_percent, right_speed_percent):
        if ( left_speed_percent > self.FORWARDS_CAP_PERCENT ):
            left_speed_percent = self.FORWARDS_CAP_PERCENT
        if ( right_speed_percent > self.FORWARDS_CAP_PERCENT ):
            right_speed_percent = self.FORWARDS_CAP_PERCENT
        self.h_motor_publisher.publish(left_speed_percent * self.motor_polarity,right_speed_percent * self.motor_polarity)
    
    def publish_to_motors_with_twist(self, left_speed_percent, right_speed_percent):
        if ( left_speed_percent > self.ANGULAR_CAP_PERCENT ):
            left_speed_percent = self.ANGULAR_CAP_PERCENT
	elif ( left_speed_percent < -1 * self.ANGULAR_CAP_PERCENT ):
            left_speed_percent = -1 * self.ANGULAR_CAP_PERCENT
        if ( right_speed_percent > self.ANGULAR_CAP_PERCENT ):
            right_speed_percent = self.ANGULAR_CAP_PERCENT
        elif ( right_speed_percent < -1 * self.ANGULAR_CAP_PERCENT ):
            right_speed_percent = -1 * self.ANGULAR_CAP_PERCENT
        self.h_motor_publisher.publish(left_speed_percent * self.motor_polarity, right_speed_percent * self.motor_polarity)
    
    def set_forwards_speed(self, speed_percent):
        if ( speed_percent > self.FORWARDS_CAP_PERCENT ):
            self.forwards_speed_percent = self.FORWARDS_CAP_PERCENT
        elif( speed_percent < -1*self.FORWARDS_CAP_PERCENT ):
            self.forwards_speed_percent = speed_percent
        else:
            self.forwards_speed_percent = speed_percent

class Vertical_Motors:

    def __init__(self):
        self.v_motor_publisher = rospy.Publisher('vertical_motors', VerticalMotors, queue_size=10)
        self.CAP_PERCENT = 60
        self.motor_polarity = 1
    
    def publish_to_motors(self, FR_speed_percent, FL_speed_percent, BR_speed_percent, BL_speed_percent):
        if ( FR_speed_percent > self.CAP_PERCENT ):
            FR_speed_percent = self.CAP_PERCENT
	elif ( FR_speed_percent < -1 * self.CAP_PERCENT ):
            FR_speed_percent = -1*self.CAP_PERCENT
        if ( FL_speed_percent > self.CAP_PERCENT ):
            FL_speed_percent = self.CAP_PERCENT
	elif ( FL_speed_percent < -1 * self.CAP_PERCENT ):
            FL_speed_percent = -1*self.CAP_PERCENT
        if ( BR_speed_percent > self.CAP_PERCENT ):
            BR_speed_percent = self.CAP_PERCENT
	elif ( BR_speed_percent < -1 * self.CAP_PERCENT ):
            BR_speed_percent = -1*self.CAP_PERCENT
        if ( BL_speed_percent > self.CAP_PERCENT ):
            BL_speed_percent = self.CAP_PERCENT
	elif ( BL_speed_percent < -1 * self.CAP_PERCENT ):
            BL_speed_percent = -1*self.CAP_PERCENT
        self.v_motor_publisher.publish( 
            FR_speed_percent * self.motor_polarity, 
            FL_speed_percent * self.motor_polarity, 
            -BR_speed_percent * self.motor_polarity, 
            -BL_speed_percent * self.motor_polarity )
