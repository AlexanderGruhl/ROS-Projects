#! /usr/bin/env python
import rospy
from odometry_package.msg import Age

rospy.init_node('cust_pub')
pub = rospy.Publisher('/any_topic_name', Age, queue_size=1)

r = rospy.Rate(10) #10hz
msg = Age()
msg.years = 19
msg.months = 5
msg.days = 23

while not rospy.is_shutdown():
    rospy.loginfo(msg)
    pub.publish(msg)
    r.sleep()