#! /usr/bin/env python

import rospkg
import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageResponse
from geometry_msgs.msg import Twist

def callback(request):
    rospy.loginfo("Starting bb8 custom movement")
    for x in range(request.repetitions * 4):
        i = 0
        while i <= request.side:
            bb8_movement.linear.x = 0.5
            bb8_movement.angular.z = 0.0
            pub.publish(bb8_movement)
            rospy.sleep(1)
            i+=1
        bb8_movement.linear.x = 0.0
        pub.publish(bb8_movement)
        rospy.sleep(2)
        bb8_movement.angular.z = 0.5
        pub.publish(bb8_movement)
        rospy.sleep(1.5)
    
    bb8_movement.linear.x = 0.0
    bb8_movement.angular.z = 0.0
    pub.publish(bb8_movement)
    response = BB8CustomServiceMessageResponse()
    response.success = True
    return response

rospy.init_node("bb8_custom_square")
bb8_movement = Twist()
bb8_custom_move_service = rospy.Service('/move_bb8_in_square_custom', BB8CustomServiceMessage, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.spin()