class VisionData():
    """Object with all the vision variables.
        does all the variable validation according to the mission at hand."""
    def __init__(self):
        self.is_dirty = False
        self.centroid = (0,0)

    def set_fields(self,visionOutObject):
        self.is_dirty = True
        x = visionOutObject.centroid_x
        y = visionOutObject.centroid_y
        self.centroid = (x,y)
        self.dice0 = ((-1,-1), (-1,-1))
        self.dice = visionOutObject.dice1
        self.dice1 = tuple(tuple(dice[:2]), tuple(dice[2:]))
        self.dice = visionOutObject.dice2
        self.dice2 = tuple(tuple(self.dice[:2]), tuple(self.dice[2:]))
        self.dice3 = ((-1,-1), (-1,-1))
        self.dice4 = ((-1,-1), (-1,-1))
        self.dice = visionOutObject.dice5
        self.dice5 = tuple(tuple(self.dice[:2]), tuple(self.dice[2:]))
        self.dice = visionOutObject.dice6
        self.dice6 = tuple(tuple(self.dice[:2]), tuple(self.dice[2:]))
        self.dices = (tuple(dice0), tuple(dice1), tuple(dice2), tuple(dice3), tuple(dice4), tuple(dice5), tuple(dice6))
        self.upper_angle = visionOutObject.upper_angle
        self.lower_angle = visionOutObject.lower_angle

    def set_dirty(self):
        self.is_dirty = True

    def set_clean(self):
        self.is_dirty = False

    def get_centroid(self):
        self.is_dirty = False
        return self.centroid

    def get_dirty(self):
        return self.is_dirty
