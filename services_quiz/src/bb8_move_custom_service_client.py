#! /usr/bin/env python

import rospkg
import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest

rospy.init_node("bb8_square_client_node")
rospy.wait_for_service('/move_bb8_in_square_custom')
bb8_square_service = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)
bb8_square_request = BB8CustomServiceMessageRequest()

bb8_square_request.side = 1.0
bb8_square_request.repetitions = 2.0
result = bb8_square_service(bb8_square_request)
print result

bb8_square_request.side = 2.0
bb8_square_request.repetitions = 1.0
result = bb8_square_service(bb8_square_request)
print result