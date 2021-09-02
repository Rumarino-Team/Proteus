#!/usr/bin/env python

import rospy
from sys import argv
from AbstractMissionNode import AbstractMissionNode
from std_msgs.msg import Float32, Bool


class SurfaceMission(AbstractMissionNode):

    def __init__(self, argv):
        super(PathMission, self).__init__("Path", Float32)
        self.default_depth = 3
        self.first_bank = -6
        self.default_motor_intensity = 30
        self.polarity_per_course = {"A" : 1, "B" : -1, "C" : -1, "D": 1} #2018 Robosub course structure
        self.course = "A"
        self.gate_time = 33
        self.surface_time = 67

    def get_vision_data(self,msg):
        pass

    def _runMission(self):
        self.auv_control._yaw_controller.set_setpoint_as_current_imu_reading()
        rospy.sleep(2)
        rospy.loginfo("Turning on depth controller")
        self.auv_control.turn_onoff_depth_controller(True, False)
        self.auv_control.go_to_depth(self.default_depth)
        rospy.sleep(2)
        rospy.loginfo("Turning on yaw controller")
        self.auv_control.turn_onoff_yaw_controller(True, False)
        self.auv_control.move_forwards_w_time(self.default_motor_intensity, self.gate_time)
        self.auv_control.pitch_degrees(self.polarity_per_course[self.course]*self.first_bank)
        self.auv_control.move_forwards_w_time(self.default_motor_intensity, self.surface_time)
        self.auv_control.stop_moving_forwards_backwards()
        self.auv_control.go_to_depth(0)
        rospy.sleep(1)
        self.auv_control.turn_onoff_controllers(False,False)
        rospy.loginfo("Finished Surface Mission Successfully")
        self.update_commander_finish()


if __name__ == '__main__':
    try:
        argv = rospy.myargv(argv)
        mission = SurfaceMission(argv)
        while not mission._activation_flag:
            continue
        mission._startMission()
    except rospy.ROSInterruptException:
        pass
