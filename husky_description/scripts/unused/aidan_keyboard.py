#!/usr/bin/env python3

import os, sys, subprocess
# print(f"---\nENV:\n{os.getenv('PATH')}\n---")
# print(f"---\n{os.uname()}\n---")
[print(f"| {a} ",end="|") for a in os.uname()]; print("\n---")
try:
    # imports required for a ROS Node
    import rospy
    from std_msgs.msg import String
    from geometry_msgs.msg import Twist
    from geometry_msgs.msg import PoseStamped
except Exception as e:
    print(f"---\nROS Node not working, ROS imports failed, with exceptio {e}\a\n---")
    

# try:
#     import keyboard
# except:
#     p = subprocess.run('pip install keyboard', shell=True, check=True, capture_output=True, encoding='utf-8')
#     print(f'Command {p.args} exited with {p.returncode} code, output: \n{p.stdout}')
#     import keyboard

import threading
from enum import Enum
import time
import numpy as np

class Gait(Enum):
    STANCE = "stance"
    TROT = "trot"


class Keyboard_Controller(object):
    def __init__(self, verbose:bool=False, linear_speed:float = 0.15, angular_speed:float = 0.5, goal:float = 0.3, offset:tuple=(0.22,0.00)):
        #Node
        rospy.init_node('keyboard_control',anonymous=False)
        
        #Publishers
        self.__pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.__pub_goal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.__pub_gait = rospy.Publisher('/keyboard/gait',String, queue_size=10)

        #Subscriber
        sub = rospy.Subscriber("/keyboard/keypress", String, self.update_key)

        #Threads 
        self.__listener_thread = None
       
        #Variables
        self.keyboard_input = None
        self.__previous_keyboard_input = None
        self.__linear_velocity_offset = offset[0]
        self.__angular_velocity_offset = offset[1]
        self.__velocity = (0,0)
        self.cmd_vel = Twist()
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed
        
        self.goal = PoseStamped()
        self.goal.pose.position.z = goal

        self.gait = Gait.STANCE

        self.verbose = verbose

    def __key_listener(self):
        while(not rospy.is_shutdown()):
            
            pass
        pass

    def start(self):
        """Start Listening"""
        self.__listener_thread = threading.Thread(target=self.__key_listener, daemon=True)
        if not self.__listener_thread.is_alive():
            self.__listener_thread.start()
            print("Listener thread started.\a")
    
    def stop(self):
        """Stop Listening"""
        if self.__listener_thread is not None and self.__listener_thread.is_alive():
            self.__listener_thread.join()
            print("Listener thread stopped.\a")
                
    def update_key(self, data:String):
        self.keyboard_input = str(data.data)
        rospy.loginfo(f"<{rospy.get_caller_id()} heard str: {data.data}>")
    
    def switch_gait(self):
        print("GAIT Changing Not Available\a\a\a")
        if self.gait == Gait.STANCE:
            self.gait = Gait.TROT
        elif self.gait == Gait.TROT:
            self.gait = Gait.STANCE
        self.__pub_gait.publish(self.gait.value)

    def set_velocity(self,linear_velocity:float=1.0, angular_velocity:float=1.0):
        
        self.cmd_vel.linear.x = linear_velocity + self.__linear_velocity_offset
        self.cmd_vel.angular.z = angular_velocity + self.__angular_velocity_offset
        self.__velocity = (linear_velocity, angular_velocity)
        # print(self.__velocity)
        self.__pub_cmd_vel.publish(self.cmd_vel)
        
        
    def run(self):
        print("---\nRunning Controller...\n---\a")
        #define rate
        rate = rospy.Rate(100)
        # self.start()
        while not rospy.is_shutdown():
            key = str(self.keyboard_input)
            print(f"<{self.keyboard_input}|{type(self.keyboard_input)}|{key}|{type(key)}>")
            self.__previous_keyboard_input = key
            # if self.keyboard_input == None or String("NONE"):
            #     print("\a")
            #     self.set_velocity(0.0, 0.0)
            
            if key == "esc":
                break
            elif key == "w":
                self.set_velocity(self.linear_speed, 0.0)
                print("forward")
            elif key == "a":
                self.set_velocity(0.00,-1*self.angular_speed)
            elif key == "s":
                self.set_velocity(0.00,-1*self.angular_speed)
            elif key == "d":
                self.set_velocity(-1*self.linear_speed, 0.0)
            elif key == "w+a":
                self.set_velocity(self.linear_speed, -1*self.angular_speed)
            elif key == "w+d":
                self.set_velocity(self.linear_speed, self.angular_speed)
            elif key == "s+a":
                self.set_velocity(-1*self.linear_speed, -1*self.angular_speed)
            elif key == "s+d":
                self.set_velocity(-1*self.linear_speed, self.angular_speed)
            elif key == "shift" and self.__previous_keyboard_input != "shift":
                self.set_velocity(0.0, 0.0)
                self.switch_gait()
            elif key == "e" and self.__previous_keyboard_input != "e":
                print("upped speed\a")
                self.linear_speed += 0.1
                if(self.linear_speed >= 10.0):
                    self.linear_speed = 10.0
                self.set_velocity(self.__velocity[0], self.__velocity[1])
            elif key == "q" and self.__previous_keyboard_input != "q":
                print("upped speed\a\a")
                self.linear_speed -= 0.1
                if(self.linear_speed <= 0.0):
                    self.linear_speed = 0.0
                self.set_velocity(self.__velocity[0], self.__velocity[1])
            else:
                print("error")
                self.set_velocity(0.10, 0.10)
            if(key is not None or ""):
                print(f"key(s)={key}, velocity={self.__velocity}")
            rate.sleep()
        # self.stop()
    
if __name__ == '__main__':
    try:
        controller = Keyboard_Controller()
        controller.run()
        
        
    except rospy.ROSInterruptException:
        pass