#!/usr/bin/env python3

class AUV_State:

    def __init__(self):
        self.is_moving_forwards = False
        self.is_moving_down = False
        self.is_absolute_heading = False
        self.current_angle = 0
        self.current_depth = 0
        self.ABSOLUTE_HEADING_MODE = 1000
