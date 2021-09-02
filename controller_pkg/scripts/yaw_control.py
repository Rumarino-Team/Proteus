#!/usr/bin/env python
#Ros import
import rospy
from controllers.pi_yaw_controller import PI_Yaw_Controller
from vehicle_control.vehicle_state import AUV_State
from vehicle_control.motors import *
#Import built in messages
from std_msgs.msg import Int32, Float32
#Import custom messages
from controller_pkg.msg import ControllerSetup, ForwardsCommand


class Yaw_Control:
    def __init__(self):
        rospy.init_node('yaw_controller')
        self.error_pub = rospy.Publisher('yaw_error', Float32, queue_size = 10)
        self.current_yaw_controller = None
        self.imu_yaw_controller = PI_Yaw_Controller(0.020,0.001,2)
        self.vision_yaw_controller = PI_Yaw_Controller(0.020,0.001,2)
        self.vision_yaw_controller.set_point = 0
        self.horizontal_motors = Horizontal_Motors()
        self.vehicle_state = AUV_State()
        self.current_vision_angle = 0
    
    def start(self):
        rospy.Subscriber('yaw_input', Float32, self.yaw_set_point_callback)
        rospy.Subscriber('yaw_current', Float32, self.yaw_measurement_callback)
        rospy.Subscriber('yaw_current_vision', Int32, self.yaw_measurement_callback_vision)
        rospy.Subscriber('forwards_command', ForwardsCommand, self.forwards_command_callback)
        rospy.Subscriber('yaw_controller_setup', ControllerSetup, self.controller_setup_callback)
        #Initialize motors to 0
        self.horizontal_motors.publish_to_motors_forwards(0,0)
        rospy.loginfo("Yaw controller successfully started")
        rospy.spin()


    def run_controller(self, current_angle_degrees):
        thrust = self.current_yaw_controller.update_controller(current_angle_degrees)
        pwm = thrust_to_pwm(thrust)
        neg_pwm = thrust_to_pwm(-1*thrust)
        percent = pwm_to_percent(pwm)
        neg_percent = pwm_to_percent(neg_pwm)
        if (self.vehicle_state.is_moving_forwards):
            self.horizontal_motors.publish_to_motors_forwards(
                int(self.horizontal_motors.forwards_speed_percent - percent), 
                int(self.horizontal_motors.forwards_speed_percent + percent))
        else:
            self.horizontal_motors.publish_to_motors_with_twist(neg_percent, percent)
        self.error_pub.publish(self.current_yaw_controller.error)


    def yaw_measurement_callback_vision(self, yaw_vision):
        #Get the current value of the vision algorithm
        self.current_vision_angle = yaw_vision.data #invert the symbol of this variable to change direction
        #If the controller is enabled run the controller
        if self.vision_yaw_controller.is_on:
            self.run_controller(self.current_vision_angle)
        #If not, turn the motors off
        else:
            self.horizontal_motors.publish_to_motors_forwards(0,0)

    """
    This function is used to initialize the controller

    @params: ControllerSetup data

    """
    def controller_setup_callback(self, controllerMSG):
        if(controllerMSG.runSenCtrl and controllerMSG.runVisCtrl):
            pass
        else:
            #Receive the value flag that turns the controller on or off
            if(controllerMSG.runSenCtrl):
                if(self.vision_yaw_controller.is_on):
                    self.imu_yaw_controller.set_point = self.vehicle_state.current_angle
                self.vision_yaw_controller.is_on = False
                self.imu_yaw_controller.is_on = True
                self.current_yaw_controller = self.imu_yaw_controller
            elif(controllerMSG.runVisCtrl):
                self.imu_yaw_controller.is_on = False
                self.vision_yaw_controller.is_on = True
                self.current_yaw_controller = self.vision_yaw_controller
            else:
                self.current_yaw_controller.is_on = False
            #Receive the gain, making sure it is greater than 0
            if controllerMSG.PGain > 0:
                self.current_yaw_controller.proportional_gain = controllerMSG.PGain
            #Receive the gain, making sure it is greater than 0
            if controllerMSG.IGain > 0:
                self.current_yaw_controller.integral_gain = controllerMSG.IGain 
            #Decide wether or not the polarity changes
            if controllerMSG.ChPolar:
                self.horizontal_motors.polarity = 1
            else:
                self.horizontal_motors.polarity = -1

        
    """
    This function sets the corresponding variables to make the AUV go forwards

    @params: ForwardsCommand data

    """
    def forwards_command_callback(self, forwardsMSG):
        #Set the motor speed
        self.horizontal_motors.set_forwards_speed(forwardsMSG.motorIntensity)
        
        #Set the forwards flag
        self.vehicle_state.is_moving_forwards = forwardsMSG.movingForwards

    
    """
    This function is used to receive a new measurement from the AHRS and, in the
    case that the controller is running it also runs the controller.

    @params: ControllerSetup data

    """

    def yaw_measurement_callback(self, yaw_imu_degrees):

        #Get the current value of the AHRS
        self.vehicle_state.current_angle = yaw_imu_degrees.data

        #If the controller is enabled run the controller
        if self.imu_yaw_controller.is_on:
            self.run_controller(yaw_imu_degrees.data)
        #If not, turn the motors off
        else:
            self.horizontal_motors.publish_to_motors_forwards(0,0)

    """
    This function is used to get a new set point from the user 

    @params: ControllerSetup data

    """
    def yaw_set_point_callback(self, angle_degrees):

        #This sets the data in Absolute heading mode
        if (int(angle_degrees.data) == self.vehicle_state.ABSOLUTE_HEADING_MODE):
            self.imu_yaw_controller.set_point = self.vehicle_state.current_angle
            self.vehicle_state.is_absolute_heading = True
        
        #This sets the data in Relative heading mode
        else :
            #Offset your current set point
            self.imu_yaw_controller.set_point -= angle_degrees.data

            #Calculate the shortest path to that set point
            if self.imu_yaw_controller.set_point > 360:
                self.imu_yaw_controller.set_point = self.imu_yaw_controller.set_point % 360
            while self.imu_yaw_controller.set_point < 0:
                self.imu_yaw_controller.set_point += 360

if __name__ == "__main__":
    controller = Yaw_Control()
    controller.start()