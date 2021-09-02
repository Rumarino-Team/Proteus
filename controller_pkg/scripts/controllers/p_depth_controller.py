#!/usr/bin/env python

from controller_abc import Controller

class P_Depth_Controller(Controller):

    def __init__(self, PGain, SensorBias):
        super(P_Depth_Controller, self).__init__(PGain)
        self.sensor_bias = SensorBias

    def update_controller(self, depth_current):
        self.error = self.set_point - depth_current
        thrust = (self.error + self.sensor_bias)*self.proportional_gain
        return thrust
