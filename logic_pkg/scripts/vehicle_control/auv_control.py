#!/usr/bin/python
import rospy
from std_msgs.msg import Float32
from vehicle_control.yaw_controller_interface import AUV_Yaw_Controller_Interface
from vehicle_control.depth_controller_interface import AUV_Depth_Controller_Interface
from vehicle_state import AUV_State

class AUV_Control:

    def __init__(self):
        self._test_mode = True
        self._yaw_controller = AUV_Yaw_Controller_Interface()
        self._depth_controller = AUV_Depth_Controller_Interface()
        self._vehicle_state = AUV_State()

    def get_depth(self):
        return self._vehicle_state.current_depth

    def get_current_angle(self):
        return self._vehicle_state.current_angle

    def pitch_degrees(self, degrees):
        if not self._test_mode:
            self._yaw_controller.change_angle_by(degrees)
        else:
            rospy.loginfo("*SIM* Pitching " + str(degrees) + " degrees")

    def go_to_depth(self, depth_in_feet):
        if not self._test_mode:
            self._depth_controller.go_to_depth(depth_in_feet)
        else:
            rospy.loginfo("*SIM* Moving to " + str(depth_in_feet) + " feet")

    def move_forwards(self, motor_intensity):
        if not self._test_mode:
            self._yaw_controller.move_forwards_backwards(-1*motor_intensity,True)
        else:
            rospy.loginfo("*SIM* Moving forwards at " + str(motor_intensity) + " intensity")
    
    def move_forwards_w_time(self, motor_intensity, time):
        if not self._test_mode:
            self._yaw_controller.move_forwards_backwards(-1*motor_intensity,True)
            rospy.sleep(time)
            self.stop_moving_forwards_backwards()
        else:
            rospy.loginfo("*SIM* Moving forwards at " + str(motor_intensity) + " intensity")
        
    def move_backwards(self, motor_intensity):
        if not self._test_mode:
            self._yaw_controller.move_forwards_backwards(motor_intensity,True)
        else:
            rospy.loginfo("*SIM* Moving forwards at " + str(motor_intensity) + " intensity")

    def stop_moving_forwards_backwards(self):
        if not self._test_mode:
            self._yaw_controller.move_forwards(0,False)
        else:
            rospy.loginfo("*SIM* Stopped Moving forwards")

    def wait_for_IMU(self):
        if not self._test_mode:
                rospy.wait_for_message('/align_current', Float32)
        else:
            rospy.loginfo("*SIM* IMU ready to use")

    def turn_onoff_controllers(self, turn_on_controllers, invert_yaw = False, invert_depth = False):
        if not self._test_mode:
            if turn_on_controllers:
                self._yaw_controller.turn_on_controller(invert_yaw)
                self._depth_controller.turn_on_controller(invert_depth)
            else:
                self._yaw_controller.turn_off_controller()
                self._depth_controller.turn_off_controller()
        else:
            rospy.loginfo("*SIM* Controllers Successfully Started")

    def turn_onoff_depth_controller(self, turn_on_controller, invert_depth):
        if not self._test_mode:
            if turn_on_controller:
                self._depth_controller.turn_on_controller(invert_depth)
            else:
                self._depth_controller.turn_off_controller()
        else:
            rospy.loginfo("*SIM* Depth Controller Successfully Started")

    def turn_onoff_yaw_controller(self, turn_on_controller, invert_yaw):
        if not self._test_mode:
            if turn_on_controller:
                self._yaw_controller.turn_on_controller(invert_yaw)
            else:
                self._yaw_controller.turn_off_controller()
        else:
            rospy.loginfo("*SIM* Yaw Controller Successfully Started")
