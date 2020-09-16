#! /usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerRequest
   
rospy.init_node("sphero_imu_client")
rospy.wait_for_service('/sphero_imu_service')
sphero_imu_service = rospy.ServiceProxy('/sphero_imu_service', Trigger)
request_object = TriggerRequest()

ctrl_c = False
def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        #self.shut_down()
        global ctrl_c
        ctrl_c = True

while not ctrl_c:
    result = sphero_imu_service(request_object)
    #rospy.loginfo(result)
    if result.success:
        #print("Success")
        pass
    else:
        print("Collision occured. Moving in " + result.message + "direction")


