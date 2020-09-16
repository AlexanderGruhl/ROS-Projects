#! /usr/bin/env python
import rospy
from nav_msgs.msg import Odometry

def callback(odo):
    #print("Position-> x: %f, y: %f, z: %f" % (odo.pose.pose.position.x, odo.pose.pose.position.y, odo.pose.pose.position.z))
    #print("Orientation-> x: %f, y: %f, z: %f" % (odo.pose.pose.orientation.x, odo.pose.pose.orientation.y, odo.pose.pose.orientation.z))
    #print("Velocity-> Linear: %f, Angular: %f" % (odo.twist.twist.linear.x, odo.twist.twist.angular.z))
    print odo

rospy.init_node('odometer_subscriber')
sub = rospy.Subscriber('/odom', Odometry, callback)
rospy.spin()
