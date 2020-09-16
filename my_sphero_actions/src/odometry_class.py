#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

class SpheroOdom():
    def __init__(self):
        self.sphero_odom_sub = rospy.Subscriber("/odom", Odometry, self.topic_callback)
        self._odom_data = Odometry()
        self.ctrl_c = False
        self.rate = rospy.Rate(1) # 1hz
        rospy.on_shutdown(self.shutdownhook)

    def topic_callback(self, odom_data):
        self._odom_data = odom_data
        rospy.logdebug(self._odom_data) 
    
    def get_odom_data(self):
        return self._odom_data
    
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.shut_down()
        self.ctrl_c = True

    def odom_sphero(self):
        while not self.ctrl_c:
            rospy.loginfo(self.get_odom_data().pose.pose.position.y)
            self.rate.sleep()

        self.shut_down()

if __name__ == '__main__':
    rospy.init_node('sphero_odom_subscriber')
    odom_obj = SpheroOdom()
    odom_obj.odom_sphero()
