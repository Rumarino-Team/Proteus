#!/usr/bin/env python

import rospy
from sys import argv
import actionlib
import threading
import time
from AbstractMissionNode import AbstractMissionNode
from DataObjects.VisionOBJ import VisionData
import common_pkg.msg as MSG


class DiceMission(AbstractMissionNode):

    def __init__(self, argv):
        super(DiceMission, self).__init__("Dice", argv)

    def _runMission(self):
        #testing
        time = 0
        while(time < 5):
            rospy.sleep(1)
            time = time + 1
            print "Dice Run"
        #end
        self._result.missioncode = 0
        return self._actionServer.set_succeeded(self._result)


if __name__ == '__main__':
    try:
        argv = rospy.myargv(argv)
        mission = DiceMission(argv)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
