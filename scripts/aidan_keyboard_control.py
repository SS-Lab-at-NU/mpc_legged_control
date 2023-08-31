#!/usr/bin/env python3

import rospy
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import threading
import keyboard
from enum import Enum
import time

class Gait(Enum):
    STANCE = "stance"
    TROT = "trot"
    

class keyboard_controller(object):
    def __init__(self):
        #Node
        rospy.init_node('keyboard_control',anonymous=False)
        
        #Publishers
        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pub_goal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.pub_gait = rospy.Publisher('/keyboard/gait',String, queue_size=10)

        #Subscriber
        # sub = rospy.Subscriber("/keyboard/keypress", String, self.update_key)

        #Threads 
        self.listener_thread = None
       
        #Variables
        self.keyboard_input = None
        self.previous_keyboard_input = None
        self.__linear_velocity_offset = 0.22
        self.__angular_velocity_offset = 0.00
        self.cmd_vel = Twist()
        self.linear_speed = 0.10
        self.angular_speed = 0.5
        self.goal = PoseStamped()
        self.goal.pose.position.z = 0.3

        self.gait = Gait.STANCE
    
    
    def __key_listener(self):
        while True:
            if keyboard.is_pressed("esc"):
                break
            if keyboard.is_pressed("r"):
                print("r pressed")
                self.keyboard_input = "space"
            elif keyboard.is_pressed("e"):
                print("E pressed")
                self.keyboard_input = "e"
            elif keyboard.is_pressed("q"):
                print("Q pressed")
                self.keyboard_input = "q"
            elif keyboard.is_pressed("w+a"):
                print("W + A pressed")
                self.keyboard_input = "w+a"
            elif keyboard.is_pressed("w+d"):
                print("W + D pressed")
                self.keyboard_input = "w+d"
            elif keyboard.is_pressed("s+a"):
                print("S + A pressed")
                self.keyboard_input = "s+a"
            elif keyboard.is_pressed("s+d"):
                print("S + D pressed")
                self.keyboard_input = "a+d"
            elif keyboard.is_pressed("w"):
                print("W pressed")
                self.keyboard_input = "w"
            elif keyboard.is_pressed("a"):
                print("A pressed")
                self.keyboard_input = "a"
            elif keyboard.is_pressed("s"):
                print("S pressed")
                self.keyboard_input = "s"
            elif keyboard.is_pressed("d"):
                print("D pressed")
                self.keyboard_input = "d"
            else:
                print("NONE")
                self.keyboard_input = None
            # time.sleep(0.01) #sleep for 10 millis for thread optimization
            pass

    def start(self):
        """Start Listening"""
        self.keyListenerThread = threading.Thread(target=self.__key_listener, daemon=True)
        if not self.keyListenerThread.is_alive():
             self.keyListenerThread.start()
    
    def stop(self):
        """Stop Listening"""
        if self.keyListenerThread is not None and self.keyListenerThread.is_alive():
             self.keyListenerThread.join()
                
    def update_key(self, data):
        # self.keyboard_input = data
        rospy.loginfo(data)
  
    def switch_gait(self):
        if self.gait == Gait.STANCE:
            self.gait = Gait.TROT
        elif self.gait == Gait.TROT:
            self.gait = Gait.STANCE
        self.pub_gait.publish(self.gait.value)

    def set_velocity(self,linear_velocity:float=0.0, angular_velocity:float=0.0):
        self.cmd_vel.linear.x = linear_velocity + self.__linear_velocity_offset
        self.cmd_vel.angular.z = angular_velocity + self.__angular_velocity_offset
        self.pub_cmd_vel.publish(self.cmd_vel)
        
        
    def run(self):
        #define rate
        rate = rospy.Rate(100)
        
        while not rospy.is_shutdown():
            self.previous_keyboard_input = self.keyboard_input
            if self.keyboard_input == None:
                self.set_velocity(0.0, 0.0)
            elif self.keyboard_input == "w":
                self.set_velocity(self.linear_speed, 0.0)
            elif self.keyboard_input == "a":
                self.set_velocity(0.00,-1*self.angular_speed)
            elif self.keyboard_input == "s":
                self.set_velocity(0.00,-1*self.angular_speed)
            elif self.keyboard_input == "d":
                self.set_velocity(-1*self.linear_speed, 0.0)
            elif self.keyboard_input == "w+a":
                self.set_velocity(self.linear_speed, -1*self.angular_speed)
            elif self.keyboard_input == "w+d":
                self.set_velocity(self.linear_speed, self.angular_speed)
            elif self.keyboard_input == "s+a":
                self.set_velocity(-1*self.linear_speed, -1*self.angular_speed)
            elif self.keyboard_input == "s+d":
                self.set_velocity(-1*self.linear_speed, self.angular_speed)
            elif self.keyboard_input == "r" and self.previous_keyboard_input != "space":
                self.switch_gait()
            elif self.keyboard_input == "e" and self.previous_keyboard_input != "e":
                self.linear_speed += 0.1
                if(self.linear_speed >= 1.0):
                    self.linear_speed = 1.0
            elif self.keyboard_input == "q"and self.previous_keyboard_input != "q":
                self.linear_speed -= 0.1
                if(self.linear_speed >= 0.0):
                    self.linear_speed = 0.0
            if(self.keyboard_input is not None):
                print(self.keyboard_input)
            rate.sleep()
    
if __name__ == '__main__':
    try:
        print("Started")
        ctrl = keyboard_controller()
        ctrl.start()
        ctrl.run()
        
        keyboard.wait("esc")
        keyboard.unhook_all()
        print("Keyboard Unhooked!")
        ctrl.stop()
        print("Thread Stopped")
    except rospy.ROSInterruptException:
        pass