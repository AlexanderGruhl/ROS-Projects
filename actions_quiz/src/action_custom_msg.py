#! /usr/bin/env python

import rospy
import time
import actionlib

from actions_quiz.msg import CustomActionMsgAction, CustomActionMsgFeedback
from std_msgs.msg import Empty

class ActionQuizClass(object):
    _feedback = CustomActionMsgFeedback()

    def __init__(self):
        self._as = actionlib.SimpleActionServer("/action_custom_msg_as", CustomActionMsgAction, self.goal_callback, False)
        self._as.start()
        self.ctrl_c = False
        self.rate = rospy.Rate(1)
       
    def launch(self):
        """function for launching the drone"""
        rospy.loginfo("Launching drone")
        while not self.ctrl_c:
            connections = self.launch_pub.get_num_connections()
            if connections > 0:
                self.launch_pub.publish(self.drone_launch_msg)
                rospy.loginfo("Publishing")
                break
            else:
                self.rate.sleep()
    
    def land(self):
        """function for landing the drone"""
        rospy.loginfo("Landing drone")
        while not self.ctrl_c:
            connections = self.land_pub.get_num_connections()
            if connections > 0:
                self.land_pub.publish(self.drone_land_msg)
                rospy.loginfo("Publishing")
                break
            else:
                self.rate.sleep()
    
    def goal_callback(self, goal):
        success = True
        r = rospy.Rate(1)
        
        self.launch_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)

        self.drone_launch_msg = Empty()
        self.drone_land_msg = Empty()

        if self._as.is_preempt_requested():
            rospy.loginfo('The goal has been cancelled/preempted')
            # the following line, sets the client in preempted state (goal cancelled)
            self._as.set_preempted()
            self.success = False

        if goal.goal == "TAKEOFF":
            self.launch()
            self._feedback.feedback = "Drone is taking off!"

        if goal.goal == "LAND":
            self.land()
            self._feedback.feedback = "Drone is landing!"

        self._as.publish_feedback(self._feedback)
        r.sleep()

        if success:
            rospy.loginfo("Success!")
            self._as.set_succeeded()    

if __name__ == '__main__':
  rospy.init_node('drone_move')
  ActionQuizClass()
  rospy.spin()