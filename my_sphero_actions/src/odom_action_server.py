#! /usr/bin/env python

import rospy
import actionlib
from my_sphero_actions.msg import record_odomAction, record_odomFeedback, record_odomResult
from nav_msgs.msg import Odometry
from odometry_class import SpheroOdom

class SpheroOdomServerClass():
    _feedback = record_odomFeedback()

    def __init__(self):
        self.sphero_action_server = actionlib.SimpleActionServer("/sphero_odom_action", record_odomAction, self.sphero_odom_callback, False)
        self.sphero_action_server.start()
        self.odom_class_postion = SpheroOdom()
        self._result = record_odomResult()
        self.ctrl_c = False
        self.rate = rospy.Rate(1)
        self.timeout = 120
    
    def sphero_odom_callback(self, goal):
        success = True
        r = rospy.Rate(1)

        #check if out of maze
        self.pos_x_pos_out_of_maze = 0.23
        self.neg_x_pos_out_of_maze = -0.56
        self.y_pos_out_of_maze = -1.85

        for i in range(self.timeout):
            rospy.loginfo("Recording Odom index="+str(i))
            if self.sphero_action_server.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                # the following line, sets the client in preempted state (goal cancelled)
                self.sphero_action_server.set_preempted()
                self.success = False
                break
            
            #if y distance greater than y_out distance then success
            if self.odom_class_postion.get_odom_data().pose.pose.position.y <= self.y_pos_out_of_maze:
                rospy.loginfo("Success!")
                break  
            else:
                rospy.loginfo(self.odom_class_postion.get_odom_data().pose.pose.position.y)
                self._result.total_distance_travelled = abs(self.odom_class_postion.get_odom_data().pose.pose.position.y)

            r.sleep()

        if success:
            rospy.loginfo("Ended")
            self.sphero_action_server.set_succeeded(self._result)    

if __name__ == '__main__':
  rospy.init_node('sphero_odom_action')
  SpheroOdomServerClass()
  rospy.spin()