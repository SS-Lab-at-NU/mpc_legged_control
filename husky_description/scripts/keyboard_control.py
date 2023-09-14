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

        self.control_pos_start_cmd = "rosrun husky_description control_pos_start.py"
        self.control_pos_stop_cmd = "rosrun husky_description control_pos_stop.py"
        self.control_wbc_start_cmd = "rosrun husky_description control_wbc_start.py"
        self.control_wbc_stop_cmd = "rosrun husky_description control_wbc_stop.py"

        self.gait = "stance"
        self.active_controller = "pos"

        self.null_speed = 0.3
        self.forward_speed = 0.35
        self.back_speed = -0.01
        self.turn_speed = 0.5

    def update_key(self, data):
        self.keyboard_input = data
        #rospy.loginfo(data)

    def set_velocity(self,linear_velocity:float=1.0, angular_velocity:float=1.0):
        self.cmd_vel.linear.x = linear_velocity
        self.cmd_vel.angular.z = angular_velocity
        # print(self.__velocity)
        self.pub_cmd_vel.publish(self.cmd_vel)

    def run(self):
        #define rate
        rate = rospy.Rate(100)

        prev_key = ""
        while not rospy.is_shutdown():
            key = self.keyboard_input
            
            if key == String("w"):
                self.set_velocity(self.forward_speed, 0.0)
            elif key == String("a"):
                self.set_velocity(self.null_speed,-1*self.turn_speed)
            elif key == String("d"):
                self.set_velocity(self.null_speed,self.turn_speed)
            elif key == String("s"):
                self.set_velocity(self.back_speed, 0.0)
            elif key == String("w+a"):
                self.set_velocity(self.forward_speed, self.turn_speed)
            elif key == String("w+d"):
                self.set_velocity(self.forward_speed, -1*self.turn_speed)
            elif key == String("s+a"):
                self.set_velocity(self.back_speed, -1*self.turn_speed)
            elif key == String("s+d"):
                self.set_velocity(self.back_speed, self.turn_speed)

            elif key == String("e") and prev_key != String("e"):
                self.null_speed += 0.01
                print("Null_speed: "+str(round(self.null_speed,2)))
            elif key == String("q") and prev_key != String("q"):
                self.null_speed -= 0.01
                print("Null_speed: "+str(round(self.null_speed,2)))
            elif key == String("e+w") and prev_key != String("e+w"):
                self.forward_speed += 0.01
                print("Forward_speed: "+str(round(self.forward_speed,2)))
            elif key == String("q+w") and prev_key != String("q+w"):
                self.forward_speed += 0.01
                print("Forward_speed: "+str(round(self.forward_speed,2)))

            elif key == String("shift") and prev_key != String("shift"):
                self.set_velocity(self.null_speed, 0.0)
                if self.gait == String("stance"):
                    self.gait = "trot"
                elif self.gait == String("trot"):
                    self.gait = "stance"
                self.pub_gait.publish(self.gait)
            elif self.keyboard_input == String("Z"):
                if self.active_controller == "wbc":
                    rospy.loginfo("WBC Deactivated")
                    self.active_controller = "pos"
                    subprocess.Popen(self.control_wbc_stop_cmd, shell=True)
                    subprocess.Popen(self.control_pos_start_cmd, shell=True)
            elif self.keyboard_input == String("X"):
                if self.active_controller == "pos":
                    rospy.loginfo("WBC Activated")
                    self.active_controller = "wbc"
                    subprocess.Popen(self.control_pos_stop_cmd, shell=True)
                    subprocess.Popen(self.control_wbc_start_cmd, shell=True)
            else:
                self.set_velocity(self.null_speed, 0.0)

            prev_key = key

            rate.sleep()
    
if __name__ == '__main__':
    try:
        ctrl = keyboard_controller()
        ctrl.run()
    except rospy.ROSInterruptException:
        pass