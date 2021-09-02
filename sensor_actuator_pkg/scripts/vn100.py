#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from vnpy import *


__vn100_path = '/dev/ttyUSB0'
__vn100_baud_rate = 115200


vn100 = EzAsyncData.connect(__vn100_path, __vn100_baud_rate)


def talker():
    rospy.init_node('vn100')
    rospy.loginfo('Initialized VN100 Node')
    pub = rospy.Publisher('yaw_current', Float32, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        value = vn100.next_data().yaw_pitch_roll.x;
        if(value < 0):
            value += 360
        pub.publish(value)
        rate.sleep()


print (__name__)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
