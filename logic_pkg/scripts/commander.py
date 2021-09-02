#!/usr/bin/env python

import rospy
import actionlib
from sys import argv
from std_msgs.msg import UInt8 as Int, Bool

ErrorMessages = { 0 : "Successfully Completed The Mission",
                  1 : "Couldn't Connect To Vision Node",
                  2 : "Couldn't Connect To Serial Node",
                  3 : "Unexpected Error"
                }

DefaultMissions = ["Gate","Path","Dice", "Qualify"]
Missions = []
currentMission = 0
ERRORCODE = 0
time_out = 900

missionTerminated = False
def finished_missions_callback(msg):
    global missionTerminated, currentMission, Missions
    rospy.loginfo("Terminated " +Missions[currentMission] +" Successfully")
    missionTerminated = msg.data

def start_Missions():
    global currentMission, missionTerminated, Missions
    rospy.loginfo("Starting Commander")
    rospy.sleep(1)
    for missionName in Missions:
        missionTopicName = "Activate" + missionName + "Mission"
        rospy.loginfo("Activating "+missionName+ " Mission")
        pub = rospy.Publisher(missionTopicName, Bool, queue_size=1)
        rospy.sleep(0.1)
        pub.publish(Bool(True))
        while not missionTerminated:
            continue
        missionTerminated = False
        currentMission += 1

if __name__ == '__main__':
    rospy.init_node("CommanderNode", anonymous = True)
    rospy.Subscriber("CommanderMissionsState", Bool, finished_missions_callback)
    argv = rospy.myargv(argv)
    try:
        if len(argv) == 1:
            Missions = DefaultMissions
        else:
            Missions = argv[1:]
            for i in range (0,len(Missions)):
                if (Missions[i].lower() == "gate"):
                    Missions[i] = "Gate"
                elif (Missions[i].lower() == "path"):
                    Missions[i] = "Path"
                elif (Missions[i].lower() == "dice"):
                    Missions[i] = "Dice"
                elif (Missions[i].lower() == "qualify"):
                    Missions[i] = "Qualify"
                elif (Missions[i].lower() == "test"):
                    Missions[i] = "Test"

    except Exception as ex:
        rospy.logerr("ERROR During Mission Select %s", ex)
    try:
        start_Missions()
        rospy.loginfo("Successfully Finished Missions COMMANDER")
    except Exception as ex:
        rospy.logerr("ERROR During Mission Execution %s", ex)
