#! /usr/bin/env python

import rospy
from imu_class import SpheroImu
from std_srvs.srv import Trigger, TriggerResponse


class SpheroImuServiceServer():
    def __init__(self):
        self.sphero_imu = SpheroImu()
        self.response = TriggerResponse()
        self.direction_determine = {"front":True, "back":True, "right":True, "left":True}
        self.counter = 0
        self.bb8_custom_move_service = rospy.Service('/sphero_imu_service', Trigger, self.imu_direction_callback) 
    
    def imu_direction_callback(self, request): 
        self.direction = self.sphero_imu.collisiondirection()
        #rospy.loginfo(self.direction)
        
        if self.direction != "nothing":   
            self.response.success = False
            self.response.message = str(self.determine_direction()) #return direction that is moved after crash
        elif self.direction == "nothing":
            self.response.success = True
            self.response.message = "Fine"
            
        return self.response
    
    def determine_direction(self):
        if self.direction == "front":
            rospy.loginfo("Going to the front")
            return "front"
        if self.direction != "back": #collide right go backwards
            rospy.loginfo("Going to the back")
            return "back"
        elif self.direction == "back":
            rospy.loginfo("Going to the left")
            return "left"
        elif self.direction == "left":
            rospy.loginfo("Going to the front")
            return "front"
        elif self.direction == "front":
            rospy.loginfo("Going to the left")
            return "right"
        
        #if self.direction_determine["front"] == False and self.direction_determine["back"] == False and
          #self.direction_determine["right"] == False and self.direction_determine["left"] == False:
             #self.direction_determine["front"] = True
             #self.direction_determine["back"] = True
             #self.direction_determine["right"] = True
             #self.direction_determine["left"] = True


if __name__ == '__main__':
    rospy.init_node("sphero_imu_server")
    sphero_service = SpheroImuServiceServer()
    rospy.spin()