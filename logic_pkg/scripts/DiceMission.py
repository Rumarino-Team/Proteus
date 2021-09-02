#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

sup
@author: Gabriel, Fernando G. & Angel

Here we are gonna start defining variables and imports
"""
#from logic_pkg.MissionObjects.Dice import Dice
from Dice import Dice
import rospy
from logic_pkg.scripts.Nodes.MissionNodes.AbstractMissionNode import AbstractMissionNode
from sys import argv
import actionlib
import threading
import time
from AbstractMissionNode import AbstractMissionNode
from DataObjects.VisionOBJ import VisionData
import common_pkg.msg as MSG

name = "Dice"


class DiceMission(AbstractMissionNode):
    def __init__(self, argv):
        super(DiceMission, self).__init__(name, argv)
        self.bounding_box_size = 50
        self.depth_interval = 0.25
        self.moving_sleep_seconds = 1
        self.moving_intensity = 40

        self.camCenterX = 640/2
        self.camCenterY = 480/2

        self.Dice1 = Dice()
        self.Dice2 = Dice()

        self.Dice1.set_boundingbox(self.bounding_box_size)
        self.Dice2.set_boundingbox(self.bounding_box_size)

    def _runMission(self):
        while self.check_pair() == 0:
            self.forward_sleep(30, 1)
        while not self.check_big_dice(self.Dice1):  # break while when dice is bigger than boundingbox
            if self.check_binding_box(self.Dice1):
                self.forward_sleep(40, 2)
            else:
                self.align(self.Dice1)
            self.update_dice(self.Dice1)
        self.align(self.Dice1)
        self.forward_sleep(40, 3)
        self.backward_sleep(40, 6)  # retrace steps
        self.update_dice(self.Dice2)
        while not self.check_big_dice(self.Dice2):  # break while when dice is bigger than boundingbox
            if self.check_binding_box(self.Dice2):
                self.forward_sleep(40, 2)
            else:
                self.align(self.Dice2)
            self.update_dice(self.Dice2)
        self.align(self.Dice2)
        self.forward_sleep(40, 3)
        self._result.missioncode = 0
        # sets finished state, end

    """"This is the self-alignment program"""
    """
    def align(self, dice):  # movement values need to be adjusted
        current_depth = self.get_depth()
        self.update_dice(dice)
        if dice.get_centx() < self.camCenterX and dice.get_centy() < self.camCenterY:
            self.left_sleep(self.moving_intensity, self.moving_sleep_seconds)
            self.go_to_depth(current_depth - self.depth_interval)
        elif dice.get_centx() < self.camCenterX and dice.get_centy() > self.camCenterY:
            self.left_sleep(self.moving_intensity, self.moving_sleep_seconds)
            self.go_to_depth(current_depth + self.depth_interval)
        elif dice.get_centx() > self.camCenterX and dice.get_centy() > self.camCenterY:
            self.right_sleep(self.moving_intensity, self.moving_sleep_seconds)
            self.go_to_depth(current_depth + self.depth_interval)
        elif dice.get_centx() > self.camCenterX and dice.get_centy() < self.camCenterY:
            self.right_sleep(self.moving_intensity, self.moving_sleep_seconds)
            self.go_to_depth(current_depth - self.depth_interval)
        elif dice.get_centx() == self.camCenterX and dice.get_centy() < self.camCenterY:
            self.go_to_depth(current_depth - self.depth_interval)
        elif dice.get_centx() == self.camCenterX and dice.get_centy() > self.camCenterY:
            self.go_to_depth(current_depth + self.depth_interval)
        elif dice.get_centx() < self.camCenterX and dice.get_centy() == self.camCenterY:
            self.left_sleep(self.moving_intensity, self.moving_sleep_seconds)
        elif dice.get_centx() > self.camCenterX and dice.get_centy() == self.camCenterY:
            self.right_sleep(self.moving_intensity, self.moving_sleep_seconds)
    """

    def align(self, dice):
        current_depth = self.get_depth()
        arguments = (self.moving_intensity, self.moving_sleep_seconds)
        if dice.centx < dice.bounding_box_left:
            self.left_sleep(*arguments)
        elif dice.centx > dice.bounding_box_right:
            self.right_sleep(*arguments)

        if dice.centy < dice.bounding_box_top:
            self.go_to_depth(current_depth + self.depth_interval)
        elif dice.centy > dice.bounding_box_bottom:
            self.go_to_depth(current_depth - self.depth_interval)

    """"Here we are gonna check all patterns possible for 7 and 11, if such pattern exists then we go with that one"""
    """
    def check_pair(self):
        visionlist = self.get_centroid()
        if visionlist[5] is not None and visionlist[6] is not None:
            self.Dice1.set_centx(visionlist[5].get_centx())  # update for vision
            self.Dice1.set_centy(visionlist[5].get_centy())  # update for vision
            self.Dice1.set_value(5)
            self.Dice1.set_boundingbox(visionlist[5].get_bounding)  # needs update
            self.Dice2.set_centx(visionlist[6].get_centx())  # update for vision
            self.Dice2.set_centy(visionlist[6].get_centy())  # update for vision
            self.Dice2.set_value(6)
            self.Dice2.set_boundingbox(visionlist[6].get_bounding)  # needs update
            return 11
        elif visionlist[6] is not None and visionlist[1]is not None:
            self.Dice1.set_centx(visionlist[1].get_centx())  # update for vision
            self.Dice1.set_centy(visionlist[1].get_centy())  # update for vision
            self.Dice1.set_value(1)
            self.Dice1.set_boundingbox(visionlist[1].get_bounding)  # needs update
            self.Dice2.set_centx(visionlist[6].get_centx())  # update for vision
            self.Dice2.set_centy(visionlist[6].get_centy())  # update for vision
            self.Dice2.set_value(6)
            self.Dice2.set_boundingbox(visionlist[6].get_bounding)  # needs update
            return 7
        elif visionlist[5] is not None and visionlist[2] is not None:
            self.Dice1.set_centx(visionlist[5].get_centx())  # update for vision
            self.Dice1.set_centy(visionlist[5].get_centy())  # update for vision
            self.Dice1.set_value(5)
            self.Dice1.set_boundingbox(visionlist[5].get_bounding)  # needs update
            self.Dice2.set_centx(visionlist[2].get_centx())  # update for vision
            self.Dice2.set_centy(visionlist[2].get_centy())  # update for vision
            self.Dice2.set_value(2)
            self.Dice2.set_boundingbox(visionlist[2].get_bounding)  # needs update
            return 7
        elif visionlist[3] is not None and visionlist[4] is not None:
            self.Dice1.set_centx(visionlist[3].get_centx())  # update for vision
            self.Dice1.set_centy(visionlist[3].get_centy())  # update for vision
            self.Dice1.set_value(3)
            self.Dice1.set_boundingbox(visionlist[3].get_bounding)  # needs update
            self.Dice2.set_centx(visionlist[4].get_centx())  # update for vision
            self.Dice2.set_centy(visionlist[4].get_centy())  # update for vision
            self.Dice2.set_value(4)
            self.Dice2.set_boundingbox(visionlist[4].get_bounding)  # needs update
            return 7
        else:
            return 0
    """
    def check_pair(self):
        visionlist = self.get_centroid()
        pairs = (
            (5, 6),
            (1, 6),
            (2, 5),
            (3, 4)
        )
        for pair in pairs:
            dice_sum = self.check_individual_pairs(visionlist, pair[0], pair[1])
            if dice_sum != 0:
                return dice_sum
        return 0

    def check_individual_pairs(self, visionlist, small_value, big_value):
            if self.dice_exists(visionlist, small_value) and self.dice_exists(visionlist, big_value):
                self.Dice1.set_centx(visionlist[small_value].get_centx())  # update for vision
                self.Dice1.set_centy(visionlist[small_value].get_centy())  # update for vision
                self.Dice1.set_value(small_value)
                self.Dice1.set_boundingbox(visionlist[small_value].get_bounding)  # needs update
                self.Dice2.set_centx(visionlist[big_value].get_centx())  # update for vision
                self.Dice2.set_centy(visionlist[big_value].get_centy())  # update for vision
                self.Dice2.set_value(big_value)
                self.Dice2.set_boundingbox(visionlist[big_value].get_bounding)  # needs update
                return small_value + big_value
            else:
                return 0

    def dice_exists(self, visionlist, value):
        x = visionlist[value][0][0]
        y = visionlist[value][0][1]
        return x != -1 and y != -1

    def check_big_dice(self, dice):  # checks 4 out of bound dice (Note: input variables)
        self.update_dice(dice)
        return dice.get_area() > dice.get_bounding_box_area()

    def forward_sleep(self, intensity, timer):
        self.forwards(True, intensity)
        time.sleep(timer)
        self.forwards(True, 0)

    def backward_sleep(self, intensity, timer):
        self.forwards(False, intensity)
        time.sleep(timer)
        self.forwards(False, 0)

    def left_sleep(self, intensity, timer):
        self.pitch_degrees(90)  # rotate 90 counterclockwise
        time.sleep(timer)
        self.forwards(True, intensity)
        time.sleep(timer)
        self.forwards(True, 0)
        self.pitch_degrees(-90)  # rotate 90 clockwise
        time.sleep(timer)

    def right_sleep(self, intensity, timer):
        self.pitch_degrees(-90)  # rotate 90 clockwise
        time.sleep(timer)
        self.forwards(True, intensity)
        time.sleep(timer)
        self.forwards(True, 0)
        self.pitch_degrees(90)  # rotate 90 counterclockwise
        time.sleep(timer)

    def update_dice(self, dice):  # update for vision
        dice_list = self.get_centroid()
        vision_dice = dice_list[dice.get_value()]
        centroid = vision_dice[0]
        dimensions = vision_dice[1]
        dice.set_centx(centroid[0])
        dice.set_centy(centroid[1])
        dice.set_dimensions(dimensions[0], dimensions[1])

    def check_binding_box(self, dice):
        self.update_dice(dice)
        if dice.bounding_box_left < dice.get_centx() < dice.bounding_box_right and dice.bounding_box_top < \
                dice.get_centy() < dice.bounding_box_bottom:
            return True
        return False

if __name__ == '__main__':
    try:
        argv = rospy.myargv(argv)
        mission = DiceMission(argv)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass