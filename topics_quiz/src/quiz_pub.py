#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
move = Twist()

def callback(data):
    f_laser = data.ranges[360]
    if(data.ranges[0] < 1):
        move.angular.z = 0.5
    elif(data.ranges[719] < 1):
        move.angular.z = 0.5
    elif(f_laser > 1):
        move.linear.x = 0.5
        move.angular.z = 0.0
    elif(f_laser < 1):
        move.linear.x = 0.2
        move.angular.z = 0.5
    
def listener():
    rospy.init_node("topics_quiz_node")
    sub = rospy.Subscriber("/kobuki/laser/scan", LaserScan, callback)
    rate = rospy.Rate(2)
    
    while not rospy.is_shutdown():
        pub.publish(move)
        rate.sleep()
        
listener()
