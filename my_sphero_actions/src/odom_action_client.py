#! /usr/bin/env python

import rospy
import actionlib
from my_sphero_actions.msg import record_odomGoal, record_odomFeedback, record_odomResult, record_odomAction
from nav_msgs.msg import Odometry

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def sphero_feedback(feedback):
    rospy.loginfo("Rec Odom Feedback feedback ==>"+str(feedback))

# initializes the action client node
rospy.init_node('sphero_action_client')

# create the connection to the action server
client = actionlib.SimpleActionClient('/sphero_odom_action', record_odomAction)
# waits until the action server is up and running
client.wait_for_server()

# creates a goal to send to the action server
goal = record_odomGoal()

# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goal, feedback_cb=sphero_feedback)

state_result = client.get_state()

rate = rospy.Rate(1)

while state_result < 2:
    rospy.loginfo("Waiting to finish: ")
    rate.sleep()
    state_result = client.get_state()
    rospy.loginfo("state_result: "+str(state_result))

state_result = client.get_state()
rospy.loginfo("[Result] State: "+str(state_result))
if state_result == ERROR:
    rospy.logerr("Something went wrong in the Server Side")
if state_result == WARN:
    rospy.logwarn("There is a warning in the Server Side")

rospy.loginfo("[Result] State: "+str(client.get_result()))
