#! /usr/bin/env python

import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

nImage = 1

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
rospy.init_node('drone_action_client')

# create the connection to the action server
client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
# waits until the action server is up and running
client.wait_for_server()

# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goal, feedback_cb=feedback_callback)

state_result = client.get_state()

rate = rospy.Rate(1)

drone_launch= Empty()
ardrone_movement = Twist()
drone_land = Empty()

launch_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
movement_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)

ardrone_movement.linear.x = 0.5
ardrone_movement.angular.z = 0.5

rospy.loginfo("Launching drone")
i=0
while not i == 3:
    launch_pub.publish(drone_launch)
    rospy.sleep(i)
    i += 1

rospy.loginfo("Moving drone")
while state_result < DONE:
    movement_pub.publish(ardrone_movement)
    state_result = client.get_state()
    rate.sleep()
    rospy.loginfo("state_result: "+str(state_result))

rospy.loginfo("[Result] State: "+str(state_result))
if state_result == ERROR:
    rospy.logerr("Something went wrong in the Server Side")
if state_result == WARN:
    rospy.logwarn("There is a warning in the Server Side")

rospy.loginfo("Landing drone")
i=0
while not i == 3:
    ardrone_movement.linear.x = 0.0
    ardrone_movement.angular.z = 0.0
    movement_pub.publish(ardrone_movement)
    land_pub.publish(drone_land)
    rospy.sleep(i)
    i += 1

#rospy.loginfo("state result: "+str(state_result))

