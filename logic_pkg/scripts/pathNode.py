#!/usr/bin/env python

import rospy
from sys import argv
from AbstractMissionNode import AbstractMissionNode
from std_msgs.msg import Float32, Bool


class PathMission(AbstractMissionNode):

    def __init__(self, argv):
        super(PathMission, self).__init__("Path", Float32)
        self.path_vision_reset_pub = rospy.Publisher("VisionPathResetData", Bool, queue_size = 2)
        self.path_detection_depth = 5

    def get_vision_data(self):
        self._vision_is_dirty = False
        return self._vision_data.data

    def _runMission(self):
        self.activate_vision()
        rospy.sleep(3)
        rospy.loginfo("Turning on depth controller")
        self.auv_control.turn_onoff_depth_controller(True, False)
        self.auv_control.go_to_depth(self.path_detection_depth)
        rospy.sleep(3)
        rospy.loginfo("Waiting for IMU")
        self.auv_control.wait_for_IMU()
        rospy.loginfo("Turning on yaw controller")
        self.auv_control.turn_onoff_yaw_controller(True, False)
        self.auv_control.move_forwards(30)
        while not self._vision_is_dirty:
            rospy.sleep(3)
        self.clear_vision_dirty_flag()
        rospy.sleep(3)
        self.auv_control.stop_moving_forwards_backwards()
        self.path_vision_reset_pub.publish(Bool(True))
        rospy.sleep(2)
        if not self._vision_is_dirty:
            rospy.logerr("Could not receive angle from vision path")
        vision_angle_degrees = self.get_vision_data()
        self.auv_control.pitch_degrees(vision_angle_degrees)
        rospy.sleep(1)
        self.auv_control.move_forwards(30)
        rospy.sleep(3)
        self.auv_control.stop_moving_forwards_backwards()
        rospy.loginfo("Finished Path Mission Successfully")
        self.deactivate_vision()
        self.update_commander_finish()


if __name__ == '__main__':
    try:
        argv = rospy.myargv(argv)
        mission = PathMission(argv)
        while not mission._activation_flag:
            continue
        mission._startMission()
    except rospy.ROSInterruptException:
        pass
