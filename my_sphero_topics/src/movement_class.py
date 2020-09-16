#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class MoveSphero():
    def __init__(self):
       self.sphero_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
       self.cmd = Twist()
       self.ctrl_c = False
       self.rate = rospy.Rate(1) # 1hz
       self.linear_speed = 0.1
       self.angular_speed = 1
       rospy.on_shutdown(self.shutdownhook)
    
    def publish_once_in_cmd_vel(self):
        while not self.ctrl_c:
            connections = self.sphero_vel_publisher.get_num_connections()
            if connections > 0:
                self.sphero_vel_publisher.publish(self.cmd)
                rospy.loginfo("Cmd Published")
                break
            else:
                self.rate.sleep()
    
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.shut_down()
        self.ctrl_c = True

    def shut_down(self):
        rospy.loginfo("Making velocity 0")
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0
        self.publish_once_in_cmd_vel()

    def move_sphero(self, direction):
        
        rospy.loginfo("Moving sphero!")

        if direction == "forwards":
            self.cmd.linear.x = self.linear_speed
            self.cmd.angular.z = 0
        elif direction == "backwards":
            self.cmd.linear.x = -self.linear_speed
            self.cmd.angular.z = 0
        elif direction == "left":
            self.cmd.linear.x = self.linear_speed
            self.cmd.angular.z = -self.angular_speed
        elif direction == "right":
            self.cmd.linear.x = 0
            self.cmd.angular.z = self.angular_speed

        while not self.ctrl_c:
            self.publish_once_in_cmd_vel()
            self.rate.sleep()

        self.shut_down()
        
if __name__ == '__main__':
    rospy.init_node('move_sphero_test')
    move_obj = MoveSphero()
    move_obj.move_sphero(direction = "forwards")
