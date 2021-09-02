#!/usr/bin/env python
#Ros import
import rospy
from controllers.p_depth_controller import P_Depth_Controller
from vehicle_control.vehicle_state import AUV_State
from vehicle_control.motors import *
#Import built in messages
from std_msgs.msg import Float32, Int32
#Import custom messages
from controller_pkg.msg import ControllerSetup


class Depth_Control:
    def __init__(self):
        rospy.init_node('depth_controller')
        self.error_pub = rospy.Publisher('depth_error', Float32, queue_size=10)
        self.current_depth_controller = None
        self.bar30_depth_controller = P_Depth_Controller(1.6, -0.6)
        self.vision_depth_controller = P_Depth_Controller(0.06, 0)
        self.vision_depth_controller.set_point = 0
        self.vertical_motors = Vertical_Motors()
        self.vehicle_state = AUV_State()
        self.current_vision_depth = 0
    
    def start(self):
        rospy.Subscriber('depth_input', Float32, self.depth_set_point_callback)
        rospy.Subscriber('depth_current', Float32, self.depth_measurement_callback)
        rospy.Subscriber('depth_current_vision', Int32, self.depth_measurement_callback_vision)
        rospy.Subscriber('depth_controller_setup', ControllerSetup, self.controller_setup_callback)
        #Initialize motors to 0
        self.vertical_motors.publish_to_motors(0,0,0,0)
        rospy.loginfo("Depth controller successfully started")
        rospy.spin()


    def run_controller(self, depth_current):
        thrust = self.current_depth_controller.update_controller(depth_current)
        pwm = thrust_to_pwm(thrust)
        percent = int(pwm_to_percent(pwm))
        self.vertical_motors.publish_to_motors(percent, percent, percent, percent)
        self.error_pub.publish(self.current_depth_controller.error)


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
                if(self.vision_depth_controller.is_on):
                    self.bar30_depth_controller.set_point = self.vehicle_state.current_depth
                self.vision_depth_controller.is_on = False
                self.bar30_depth_controller.is_on = True
                self.current_depth_controller = self.bar30_depth_controller
            elif(controllerMSG.runVisCtrl):
                self.bar30_depth_controller.is_on = False
                self.vision_depth_controller.is_on = True
                self.current_depth_controller = self.vision_depth_controller
            else:
                self.current_depth_controller.is_on = False
            #Receive the gain, making sure it is greater than 0
            if controllerMSG.PGain > 0:
                self.current_depth_controller.proportional_gain = controllerMSG.PGain
            #Receive the gain, making sure it is greater than 0
            if controllerMSG.IGain > 0:
                self.current_depth_controller.integral_gain = controllerMSG.IGain 
            #Decide wether or not the polarity changes
            if controllerMSG.ChPolar:
                self.vertical_motors.polarity = 1
            else:
                self.vertical_motors.polarity = -1
    

    """
    This function is used to receive a new measurement from the AHRS and, in the
    case that the controller is running it also runs the controller.

    @params: ControllerSetup data

    """

    def depth_measurement_callback_vision(self, depth_vision_measurement):

        #Get the current value of the AHRS
        self.current_vision_depth = depth_vision_measurement.data
        if self.vision_depth_controller.is_on:
            self.run_controller(self.current_vision_depth)
        else:
            self.vertical_motors.publish_to_motors(0,0,0,0)

    """
    This function is used to receive a new measurement from the AHRS and, in the
    case that the controller is running it also runs the controller.

    @params: ControllerSetup data

    """

    def depth_measurement_callback(self, depth_sensor_measurement):

        #Get the current value of the AHRS
        self.vehicle_state.current_depth = depth_sensor_measurement.data
        depth_current = depth_sensor_measurement.data
        if self.bar30_depth_controller.is_on:
            self.run_controller(depth_current)
        else:
            self.vertical_motors.publish_to_motors(0,0,0,0)

    """
    This function is used to get a new set point from the user 

    @params: ControllerSetup data

    """
    def depth_set_point_callback(self, depth_set_point):
        self.bar30_depth_controller.set_point = depth_set_point.data

if __name__ == "__main__":
    controller = Depth_Control()
    controller.start()
