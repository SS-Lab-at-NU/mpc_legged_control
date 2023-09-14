#!/usr/bin/env python3

import rospy
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String

class position_control(object):
    def __init__(self):
        #Node
        rospy.init_node('joint_cmd',anonymous=False)
        
        #Publishers
        self.pub_fr_hip_frontal = rospy.Publisher('/husky/fr_hip_frontal_position_controller/command', Float64, queue_size=10)
        self.pub_fr_hip_sagittal = rospy.Publisher('/husky/fr_hip_sagittal_position_controller/command', Float64, queue_size=10)
        self.pub_fr_knee = rospy.Publisher('/husky/fr_knee_position_controller/command', Float64, queue_size=10)
        self.pub_br_hip_frontal = rospy.Publisher('/husky/br_hip_frontal_position_controller/command', Float64, queue_size=10)
        self.pub_br_hip_sagittal = rospy.Publisher('/husky/br_hip_sagittal_position_controller/command', Float64, queue_size=10)
        self.pub_br_knee = rospy.Publisher('/husky/br_knee_position_controller/command', Float64, queue_size=10)

        self.pub_fl_hip_frontal = rospy.Publisher('/husky/fl_hip_frontal_position_controller/command', Float64, queue_size=10)
        self.pub_fl_hip_sagittal = rospy.Publisher('/husky/fl_hip_sagittal_position_controller/command', Float64, queue_size=10)
        self.pub_fl_knee = rospy.Publisher('/husky/fl_knee_position_controller/command', Float64, queue_size=10)
        self.pub_bl_hip_frontal = rospy.Publisher('/husky/bl_hip_frontal_position_controller/command', Float64, queue_size=10)
        self.pub_bl_hip_sagittal = rospy.Publisher('/husky/bl_hip_sagittal_position_controller/command', Float64, queue_size=10)
        self.pub_bl_knee = rospy.Publisher('/husky/bl_knee_position_controller/command', Float64, queue_size=10)



    def run(self):
        #define rate
        rate = rospy.Rate(100)

        while not rospy.is_shutdown():
            self.pub_fr_hip_frontal.publish(0)
            self.pub_fr_hip_sagittal.publish(0)
            self.pub_fr_knee.publish(0)
            self.pub_br_hip_frontal.publish(0)
            self.pub_br_hip_sagittal.publish(0)
            self.pub_br_knee.publish(0)

            self.pub_fl_hip_frontal.publish(0)
            self.pub_fl_hip_sagittal.publish(0)
            self.pub_fl_knee.publish(0)
            self.pub_bl_hip_frontal.publish(0)
            self.pub_bl_hip_sagittal.publish(0)
            self.pub_bl_knee.publish(0)
            rate.sleep()

    
if __name__ == '__main__':
    try:
        thing = position_control()
        thing.run()
    except rospy.ROSInterruptException:
        pass