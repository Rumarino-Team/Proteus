#!/usr/bin/env python

import rospy
from sys import argv
import actionlib
import threading
import time
from AbstractMissionNode import AbstractMissionNode
import common_pkg.msg as MSG

speed = 40
gate_depth = 3
dice_depth = 7
first_bank = -6
second_bank = -30
first_gate_time = 33
dice_time = 30

surface_time = 67

generic_sleep = 4
dive_sleep = 8

bias = -0.7
name = "Qualify"
polarity = {"A" : 1, "B" : -1, "C" : -1, "D": 1}
course_letter = "D"

class QualifyMission(AbstractMissionNode):
    
    

    def __init__(self, argv):
        super(QualifyMission, self).__init__(name, argv)


    def _runMission(self):
        rospy.sleep(5)
        self.pitch_degrees(1000)
        self.pitch_degrees(180)
        self.turn_on_depth_controllers(True, False)
        self.go_to_depth(gate_depth)
        """while(self.get_depth() - bias > gate_depth*1.2 or self.get_depth() - bias < gate_depth*0.8):
            print("Looping to turn on depth controller: {} current depth, {} desired depth".format(self.get_depth(), gate_depth))
            self.turn_on_depth_controllers(True, False)
            self.go_to_depth(gate_depth)
            rospy.sleep(1)""" 
        
        print("Waiting for IMU")
        self.wait_for_IMU()
        print("Turning on align controller")
        self.turn_on_align_controllers(True, False)
        self.move(speed, first_gate_time)
        self.pitch_degrees(polarity[course_letter]*first_bank)
        self.move(speed, surface_time)
        self.go_to_depth(0)
        """self.go_to_depth(dice_depth)
        rospy.sleep(generic_sleep) 
        self.pitch_degrees(14)
        rospy.sleep(generic_sleep)
        self.pitch_degrees(-14)
        rospy.sleep(generic_sleep)
        self.pitch_degrees(polarity[course_letter]*first_bank)
        rospy.sleep(dive_sleep)
        self.move(speed, dice_time)
        rospy.sleep(2)
        self.pitch_degrees(14)
        rospy.sleep(generic_sleep)
        self.pitch_degrees(-14)
        self.pitch_degrees(polarity[course_letter]*second_bank)
        rospy.sleep(generic_sleep) 
        self.move(speed, 20)"""
        self.turn_on_controllers(False,False,False)
        print("Mission complete, returning...")

    def move(self, intensity, interval):
        print("moving...")
        self.forwards(True, intensity)
        rospy.sleep(interval)
        self.forwards(False, 0)


if __name__ == "__main__":
    try:
        argv = rospy.myargv(argv)
        mission = QualifyMission(argv)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
