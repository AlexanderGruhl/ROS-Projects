#! /usr/bin/env python

import rospy
import time
import actionlib

from actionlib.msg import TestAction, TestActionFeedback, TestActionResult
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

class DroneMoveClass(object):
    _feedback = TestActionFeedback()
    _result = TestActionResult()

    def __init__(self):
        self._as = actionlib.SimpleActionServer("drone_move_as", TestAction, self.goal_callback, False)
        self._as.start()
        self.ctrl_c = False
        self.rate = rospy.Rate(10)

    def publish_once_in_movement_pub(self, cmd):
        """
        This is because publishing in topics sometimes fails teh first time you publish.
        In continuos publishing systems there is no big deal but in systems that publish only
        once it IS very important.
        """
        while not self.ctrl_c:
            connections = self.movement_pub.get_num_connections()
            if connections > 0:
                self.movement_pub.publish(cmd)
                rospy.loginfo("Publish in cmd_vel...")
                break
            else:
                self.rate.sleep()
    
    def moveforward(self):
        self.drone_movement_msg.linear.x = 1.0
        self.drone_movement_msg.angular.z = 0
        self.publish_once_in_movement_pub(self.drone_movement_msg)
    
    def turn(self):
        self.drone_movement_msg.linear.x = 0
        self.drone_movement_msg.angular.z = 1.0
        self.publish_once_in_movement_pub(self.drone_movement_msg)

    def stop(self):
        self.drone_movement_msg.linear.x = 0
        self.drone_movement_msg.angular.z = 0
        self.publish_once_in_movement_pub(self.drone_movement_msg)

    def goal_callback(self, goal):
        success = True
        r = rospy.Rate(1)
        
        self.launch_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.movement_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)

        self.drone_launch_msg = Empty()
        self.drone_movement_msg = Twist()
        self.drone_land_msg = Empty()

        rospy.loginfo("Launching drone")
        i=0
        while not i == 3:
            self.launch_pub.publish(self.drone_launch_msg)
            time.sleep(i)
            i += 1

        self.side_time = goal.goal
        self.turn_time = 1.8

        rospy.loginfo("Moving drone")
        for x in range(4):

            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                # the following line, sets the client in preempted state (goal cancelled)
                self._as.set_preempted()
                self.success = False
                break
            
            self.moveforward()
            time.sleep(self.side_time)
            self.turn()
            time.sleep(self.turn_time)
            
            self._feedback.feedback = x
            self._as.publish_feedback(self._feedback)
            r.sleep()


        rospy.loginfo("Landing drone")
        self.stop()
        i=0
        while not i == 3:
            self.land_pub.publish(self.drone_land_msg)
            time.sleep(i)
            i += 1
        
        if success:
            self._result.result = (self.side_time * 4) + (self.turn_time * 4)
            rospy.loginfo("Success! It took %d long to fly in the squre", self._result.result)
            self._as.set_succeeded(self._result)


if __name__ == '__main__':
  rospy.init_node('drone_move')
  DroneMoveClass()
  rospy.spin()