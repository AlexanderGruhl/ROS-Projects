#! /usr/bin/env python

import rospkg
import rospy
from geometry_msgs.msg import Twist
from unit_4_services.srv import move_bb8_in_circle_custom, move_bb8_in_circle_customResponse

def callback(data):
    rospy.loginfo("Starting bb8 custom movement")
    bb8_movement.linear.x = 0.5
    bb8_movement.angular.z = 0.5
    i = 0
    while i <= data.duration:
        pub.publish(bb8_movement)
        rospy.sleep(1)
        i+=1
    bb8_movement.linear.x = 0.0
    bb8_movement.angular.z = 0.0
    pub.publish(bb8_movement)
    response = move_bb8_in_circle_customResponse()
    response.sucess = True
    return response

rospy.init_node("bb8_custom_circle")
bb8_movement = Twist()
bb8_custom_move_service = rospy.Service('/move_bb8_in_circle_custom', move_bb8_in_circle_custom, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.spin()
