#!/usr/bin/env python3

import rospy
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

import subprocess

class keyboard_controller(object):
    def __init__(self):
        #Node
        rospy.init_node('keyboard_control',anonymous=False)
        
        #Publishers
        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pub_goal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.pub_gait = rospy.Publisher('/keyboard/gait',String, queue_size=10)

        #Subscriber
        sub = rospy.Subscriber("/keyboard/keypress", String, self.update_key)

        #Variables
        self.keyboard_input = ""
        
        self.cmd_vel = Twist()

        self.goal = PoseStamped()
        self.goal.pose.position.z = 0.3

        self.control_pos_start_path = "control_pos_start.py"
        self.control_pos_stop_path = "control_pos_stop.py"
        self.control_wbc_start_path = "control_wbc_start.py"
        self.control_wbc_stop_path = "control_wbc_stop.py"

        self.gait = "stance"
        self.active_controller = "pos"

    def update_key(self, data):
        self.keyboard_input = data
        rospy.loginfo(data)

    def run(self):
        #define rate
        rate = rospy.Rate(100)

        while not rospy.is_shutdown():
            if self.keyboard_input == String(""):
                self.cmd_vel.linear.x = 0.22
                self.cmd_vel.angular.z = 0.0

            if self.keyboard_input == String(","):
                self.cmd_vel.linear.x = 0.32
            elif self.keyboard_input == String("o"):
                self.cmd_vel.linear.x = -0.01

            if self.keyboard_input == String("e"):
                self.cmd_vel.angular.z = -0.5
            elif self.keyboard_input == String("a"):
                self.cmd_vel.angular.z = 0.5


            self.pub_cmd_vel.publish(self.cmd_vel)
            #self.pub_goal.publish(self.goal)

            if self.keyboard_input == String("u"):
                if self.gait == "stance":
                    self.gait = "trot"
                elif self.gait == "trot":
                    self.gait = "stance"
                self.pub_gait.publish(self.gait)

            if self.keyboard_input == String("1"):
                if self.active_controller == "wbc":
                    rospy.loginfo("WBC Deactivated")
                    self.active_controller = "pos"
                    subprocess.call(["python3",self.control_wbc_stop_path])
                    subprocess.call(["python3",self.control_pos_start_path])
            elif self.keyboard_input == String("2"):
                if self.active_controller == "pos":
                    rospy.loginfo("WBC Activated")
                    self.active_controller = "wbc"
                    subprocess.call(["python3",self.control_pos_stop_path])
                    subprocess.call(["python3",self.control_wbc_start_path])

            rate.sleep()
    
if __name__ == '__main__':
    try:
        ctrl = keyboard_controller()
        ctrl.run()
    except rospy.ROSInterruptException:
        pass