"""
@author: Fernando Guzman and Angel Burgos
"""

class Gate:
    def __init__(self):
        self.center_leftx = 0
        self.center_lefty = 0

        self.center_rightx = 0
        self.center_righty = 0

        self.centerx = 0
        self.centery = 0

        self.distance = 0

    def set_center_leftx(self, x):
        self.center_leftx = x

    def set_center_lefty(self, y):
        self.center_lefty = y

    def set_center_rightx(self, x):
        self.center_rightx = x

    def set_center_righty(self, y):
        self.center_righty = y

    def set_centerx(self, x):
        self.centerx = x

    def set_centery(self, y):
        self.centery = y

    def set_distance(self, d):
        self.distance = d

    def get_center_leftx(self):
        return self.center_leftx

    def get_center_lefty(self):
        return self.center_lefty

    def get_center_rightx(self):
        return self.center_rightx

    def get_center_righty(self):
        return self.center_righty

    def get_centerx(self):
        return self.centerx

    def get_centery(self):
        return self.centery

    def get_distance(self):
        return self.distance