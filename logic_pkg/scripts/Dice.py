#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

;)
@author: Gabriel Valentin
"""


class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


class Dice:
    def __init__(self):

        self.width = 0
        self.height = 0

        self.centx = 0
        self.centy = 0
        self.bounding_box_size = 0
        self.bounding_box_top = 0
        self.bounding_box_left = 0
        self.bounding_box_right = 0
        self.bounding_box_bottom = 0
        self.value = 0

        self.cam_center = Point(640/2.0, 480/2.0)

    def set_centx(self, centx):
        self.centx = centx

    def set_centy(self, centy):
        self.centy = centy

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def set_bounding(self, bounding_box_size):
        self.bounding_box_size = bounding_box_size
        self.bounding_box_top = self.cam_center.y - self.bounding_box_size
        self.bounding_box_left = self.cam_center.x - self.bounding_box_size
        self.bounding_box_right = self.cam_center.x + self.bounding_box_size
        self.bounding_box_bottom = self.cam_center.y + self.bounding_box_size

    def get_bounding_box_area(self):
        return (self.bounding_box_size*2)**2

    def set_value(self, value):
        self.value = value

    def get_centx(self):
        return self.centx

    def get_centy(self):
        return self.centy

    def get_bounding(self):
        return self.bounding_box_size

    def get_value(self):
        return self.value

    def get_area(self):
        return self.width*self.height
