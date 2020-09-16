#! /usr/bin/env python

import rospy
from std_msgs.msg import Int32

rospy.init_node("publisher_node")
pub = rospy.Publisher("simple_topic", Int32, queue_size=1)
rate = rospy.Rate(2)
count = Int32()
count.data = 0

while not rospy.is_shutdown():
    pub.publish(count)
    count.data += 1
    rate.sleep()