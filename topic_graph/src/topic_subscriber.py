#! /usr/bin/env python

import rospy
from std_msgs.msg import Int32

def simple_callback(msg):
    print msg.data


rospy.init_node("subscriber_node")
sub = rospy.Subscriber("simple_topic", Int32, simple_callback)
rospy.spin()
