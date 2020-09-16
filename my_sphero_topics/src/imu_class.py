#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

class SpheroImu():
    def __init__(self):
        self.sphero_imu_sub = rospy.Subscriber("/sphero/imu/data3", Imu, self.get_sphero_imu)
        self._imu_data = Imu()
        self.threshold = 7.0
        self.ctrl_c = False
        self.rate = rospy.Rate(1) # 1hz
        rospy.on_shutdown(self.shutdownhook)

    def get_sphero_imu(self, imu_data):
        self._imu_data = imu_data
        self.collisiondirection()
        rospy.logdebug(self._imu_data)  
    
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        #self.shut_down()
        self.ctrl_c = True

    def collisiondirection(self):     
        self.x_collision = self._imu_data.linear_acceleration.x
        self.y_collision = self._imu_data.linear_acceleration.y
        self.z_collision = self._imu_data.linear_acceleration.z

        if abs(self.x_collision) > self.threshold or abs(self.y_collision) > self.threshold or abs(self.z_collision > self.threshold):
            if abs(self.x_collision) > abs(self.y_collision) and abs(self.x_collision) > abs(self.z_collision):
                rospy.loginfo("Side (x axis) collision")
                if self.x_collision > 0:
                    collision = "right"
                else:
                    collision = "left"
                #rospy.loginfo(self.collision)
                return collision
            elif abs(self.y_collision) > abs(self.x_collision) and abs(self.y_collision) > abs(self.z_collision):
                rospy.loginfo("Front (y axis) collision")
                if self.y_collision > 0:
                    collision = "front"
                else:
                    collision = "back"
                return collision
            elif abs(self.z_collision) > abs(self.x_collision) and abs(self.z_collision) > abs(self.y_collision):
                rospy.loginfo("Vertical (z axis) collision")
                if self.z_collision > 0:
                    collision = "top"
                else:
                    collision = "bottom"
                return collision
        else:
            collision = "nothing"
            return collision
        

    
    def imu_sphero(self):
        while not self.ctrl_c:
            #rospy.loginfo(self._imu_data)
            rospy.loginfo(self.collision)
            self.rate.sleep()

        self.shut_down()

if __name__ == '__main__':
    rospy.init_node('sphero_imu_subscriber')
    imu_obj = SpheroImu()
    imu_obj.imu_sphero()
