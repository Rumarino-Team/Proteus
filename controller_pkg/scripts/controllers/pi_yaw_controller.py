#!/usr/bin/env python

from controller_abc import Controller

class PI_Yaw_Controller(Controller):

    def __init__(self, PGain, IGain,IntegralActiveZone):
        super(PI_Yaw_Controller, self).__init__(PGain, IGain)
        self.integral_active_zone = IntegralActiveZone

    def update_controller(self, current_angle):
        
        #Calculate the error from the set point and the current yaw value
        self.error = self.set_point - current_angle
        #Get shortest path
        if self.error > 180:
            self.error -= 360
        elif self.error < -180:
            self.error += 360

        if(abs(self.error) <= abs(self.integral_active_zone) and abs(self.error) - self.epsilon > 0):
            self.integral_term += self.error
        else:
            self.integral_term = 0
        
        self.proportional_term = self.error
        thrust = (self.proportional_gain * self.proportional_term) + (self.integral_gain * self.integral_term)

        return thrust
