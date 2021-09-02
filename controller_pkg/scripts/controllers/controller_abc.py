#!/usr/bin/env python
from abc import ABCMeta, abstractmethod

class Controller:
    __metaclass__ = ABCMeta
    def __init__(self, PGain = 0, IGain = 0, DGain = 0):
        self.proportional_gain = PGain
        self.integral_gain = IGain
        self.differential_gain = DGain
        self.proportional_term = 0
        self.integral_term = 0
        self.differential_term = 0
        self.error = 0
        self.set_point = 0
        self.epsilon = 0.001
        self.is_on = False
    
    @abstractmethod
    def update_controller(self, current_value):
        raise Exception('Unimplemented method update_controller')
    
    def set_p_gain(self, PGain):
        self.proportional_gain = PGain
    
    def set_i_gain(self, IGain):
        self.integral_gain = IGain
    
    def set_d_gain(self, DGain):
        self.differential_gain = DGain