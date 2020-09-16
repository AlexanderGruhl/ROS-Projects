#! /usr/bin/env python

import rospkg
import rospy
from std_srvs.srv import Empty, EmptyRequest

rospy.init_node('bb8_service_client_node')
rospy.wait_for_service('/move_bb8_in_circle')
bb8_circle_service = rospy.ServiceProxy('/move_bb8_in_circle', Empty)
bb8_circle_object = EmptyRequest()

result = bb8_circle_service(bb8_circle_object)
print result