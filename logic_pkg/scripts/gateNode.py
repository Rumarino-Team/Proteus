#!/usr/bin/env python

import rospy
from sys import argv
import actionlib
import threading
import time
from Gate import Gate
from AbstractMissionNode import AbstractMissionNode
import common_pkg.msg as MSG


name = "Gate"

class GateMission(AbstractMissionNode):
    
    

    def __init__(self, argv):
        super(GateMission, self).__init__(name, argv)

#Calibration Box
#-------------------------------------------------------------------------------------------------------
        self.camCenterX = 640/2
        self.camCenterY = 480/2
        self.bounding_box_size = 50
        self.align_interval = 2
        self.desired_depth = 4
        self.motor_intensity = -20
        self.approach_time_interval = 2
        self.ros_variable_refresh_rate = 0.15
        self.exit_time_interval = 6
        self.initial_sweep_search_degrees = -70
#--------------------------------------------------------------------------------------------------------
        self.bounding_box_left_edge = self.camCenterX - self.bounding_box_size
        self.bounding_box_right_edge = self.camCenterX + self.bounding_box_size
        self.gate = Gate()
        self.gate.set_centerx(-1)
        self.gate.set_centery(-1)


    def _runMission(self):
        print("Selecting Vision Mission: " + name)
        print("Turning on controllers")
        self.wait_for_IMU()
        time.sleep(2)
        self.pitch_degrees(1000.0)
        self.turn_on_controllers(True, False, False)
        #MUST UN COMMENT NEXT LINE
        #self.select_vision_mission(name, 'front', 0)
        self.select_vision_mission("Bouy", 'front', 0)
        print("Starting Gate Mission...")
        print("Diving to: " + str(self.desired_depth))
        # current_depth = self.get_depth()
        current_depth = 4	#Testing hardcoded
        self.go_to_depth(self.desired_depth)
        print("Looping while not at desired depth...")
        while self.desired_depth > current_depth:  # fix
            print("looping while not at desired depth...")
            current_depth = self.get_depth()
        print("calling see gate...")
        self.see_gate()
        print("Looping while vision is dirty...")
        while self.is_vision_dirty():
            print("looping")
            if self.check_bounding_box():
                self.move(self.motor_intensity, self.approach_time_interval)
            else:
                self.align_with_centroid()
            self.set_center()
            time.sleep(self.ros_variable_refresh_rate)
        self.move(self.motor_intensity, self.exit_time_interval)
        self._result.missioncode = 0
        print("Mission complete, returning...")

    def set_center(self):
        print("setting center...")
        centroid = self.get_centroid()
        print(centroid[0], centroid[1])
        self.gate.set_centerx(centroid[0])
        self.gate.set_centery(centroid[1])

    def check_bounding_box(self):
        print("checking bounding box")
        self.set_center()
        return (self.camCenterX-self.bounding_box_size) < self.gate.get_centerx() < (self.camCenterX + self.bounding_box_size) and \
            (self.camCenterY - self.bounding_box_size) < self.gate.get_centery() < (self.camCenterY + self.bounding_box_size)

    def align_with_centroid(self):
        print("aligning with centroid...")
        is_aligned = False
        print("Looping is not aligned...")
        while not is_aligned:
            print("looping...")
            centroid = self.get_centroid()
            if centroid[0] < self.bounding_box_left_edge:
                self.pitch_degrees(self.align_interval)
            elif centroid[0] > self.bounding_box_right_edge:
                self.pitch_degrees(-self.align_interval)
            else:
                is_aligned = True
                self.pitch_degrees(1000.0)
                print("auv is aligned, breaking...")
            time.sleep(self.approach_time_interval)

    def see_gate(self):
        print("trying to see gate...")
        self.set_center()
        print("Looping while vision is not dirty")
        while not self.is_vision_dirty():
            self.pitch_degrees(self.initial_sweep_search_degrees)
            self.set_center()
            time.sleep(self.approach_time_interval)

    def move(self, intensity, interval):
        print("moving...")
        self.forwards(True, intensity)
        time.sleep(interval)
        self.forwards(True, 0)


if __name__ == "__main__":
    try:
        argv = rospy.myargv(argv)
        mission = GateMission(argv)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
