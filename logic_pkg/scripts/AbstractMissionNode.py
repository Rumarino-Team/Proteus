#!/usr/bin/env python

import abc
import rospy
from std_msgs.msg import Float32, String, Bool
from vehicle_control.auv_control import AUV_Control


class AbstractMissionNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, vision_message_type):
        rospy.init_node(name + 'Node')
        self.auv_control = AUV_Control()
        self._test_mode = False
        self._name = name
        self._vision_is_dirty = False
        self._activation_flag = False
        self._finished_mission_pub = rospy.Publisher("CommanderMissionsState", Bool, queue_size = 2)
        self._activate_mission_sub = rospy.Subscriber("Activate"+self._name+"Mission", Bool, self.activate_mission_callback)
        self._activate_vision_pub = rospy.Publisher("Activate"+self._name+"Vision", Bool, queue_size = 1)
        self._vision_data = vision_message_type()
        rospy.Subscriber("Vision"+name+"Output", vision_message_type, self.vision_callback)
        rospy.loginfo(name + " Node Successfully Initialized.")

    def _startMission(self):
        rospy.loginfo(self._name + " Mission started")
        self._runMission()
        rospy.loginfo("Successfully Finish "+ self._name + " Mission")

    def vision_callback(self, vision_msg):
        self._vision_is_dirty = True
        self._vision_data = vision_msg
    
    def clear_vision_dirty_flag(self):
        self._vision_is_dirty = False

    def activate_mission_callback(self, msg):
        rospy.loginfo(self._name+" Mission Activated")
        self._activation_flag = msg.data

    def update_commander_finish(self):
        self._finished_mission_pub.publish(True)

    @abc.abstractmethod
    def get_vision_data(self):
        """
        Returns the vision data
        """

    def activate_vision(self):
        self._activate_vision_pub.publish(True)
    
    def deactivate_vision(self):
        self._activate_vision_pub.publish(False)

    @abc.abstractmethod
    def _runMission(self):
        """
        Runs the mission code
        """


if __name__ == '__main__':
    pass
