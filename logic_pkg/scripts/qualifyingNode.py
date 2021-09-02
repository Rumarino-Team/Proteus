#!/usr/bin/env python

import rospy
from common_pkg.srv import *

MISSIONCODE = 0

def _startMission(state):
    rospy.loginfo("QualifyingServerNode Received message %s from Commander" % state)
    try:
        rospy.loginfo("Successfully Finish Qualifying Mission" )
        #Start Path Mission
        #_RunPathMission()
    except Exception as e:
        errorcode, errormessage = e.args
        rospy.logerr("ERRORCODE %d: "+ errormessage + " in Qualifying mission", errorcode)
    finally:
        return RunMissionResponse(MISSIONCODE)


def qualifying_Server():
    rospy.init_node('QualifyingServerNode', anonymous = True)
    service = rospy.Service('startQualifyingMission', RunMission, _startMission)
    rospy.loginfo("Qualifying Server Successfully Initialized.")
    rospy.spin()

if __name__ == '__main__':
    try:
        qualifying_Server()
    except rospy.ROSInterruptException:
        pass
