#!/usr/bin/env python3
try:
    # imports required for a ROS Node
    import rospy
    from std_msgs.msg import String
    from geometry_msgs.msg import Twist
    from geometry_msgs.msg import PoseStamped
    print("---\nRosnode imports succceeded!\a\a")
except:
    print("---\nRosnode imports failed.\n---\a")
    ModuleNotFoundError()

import os, sys, subprocess
print(os.getenv('PATH'))
print(os.uname())

try:
    import keyboard
except:
    print("---\nkeyboard library not installed, installing keyboard...\a")
    p = subprocess.run('pip install keyboard', shell=True, check=True, capture_output=True, encoding='utf-8')
    print(f'Command {p.args} exited with {p.returncode} code, output: \n{p.stdout}\n---\a\a')
    import keyboard

import threading
import time
import numpy as np

class KeyListener(object):
    def __init__(self, verbose:bool=True):
        #Node
        rospy.init_node('keyboard') # rospy.init_node('keyboard',anonymous=False)
        
        #Publishers
        self.__pub_key = rospy.Publisher('keyboard/keypress', String, queue_size=10)
        
        #Subscriber
        # sub = rospy.Subscriber("/keyboard/keypress", String, self.update_key)

        #Threads 
        self.__listener_thread = None
       
        #Variables
        self.__keyboard_input = None
        self.verbose = verbose

    def __key_listener(self):
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            if keyboard.is_pressed("shift"):
                if(self.verbose): print("shift pressed")
                self.__keyboard_input = "shift"

            elif keyboard.is_pressed("e+w"):
                if(self.verbose): print("E + W pressed")
                self.__keyboard_input = "e+w"
            elif keyboard.is_pressed("q+w"):
                if(self.verbose): print("Q + W pressed")
                self.__keyboard_input = "q+w"

            elif keyboard.is_pressed("e"):
                if(self.verbose): print("E pressed")
                self.__keyboard_input = "e"
            elif keyboard.is_pressed("q"):
                if(self.verbose): print("Q pressed")
                self.__keyboard_input = "q"

            elif keyboard.is_pressed("w+a"):
                if(self.verbose): print("W + A pressed")
                self.__keyboard_input = "w+a"
            elif keyboard.is_pressed("w+d"):
                if(self.verbose): print("W + D pressed")
                self.__keyboard_input = "w+d"
            elif keyboard.is_pressed("s+a"):
                if(self.verbose): print("S + A pressed")
                self.__keyboard_input = "s+a"
            elif keyboard.is_pressed("s+d"):
                if(self.verbose): print("S + D pressed")
                self.__keyboard_input = "s+d"
                
            elif keyboard.is_pressed("w"):
                if(self.verbose): print("W pressed")
                self.__keyboard_input = "w"
            elif keyboard.is_pressed("a"):
                if(self.verbose): print("A pressed")
                self.__keyboard_input = "a"
            elif keyboard.is_pressed("s"):
                if(self.verbose): print("S pressed")
                self.__keyboard_input = "s"
            elif keyboard.is_pressed("d"):
                if(self.verbose): print("D pressed")
                self.__keyboard_input = "d"
            elif keyboard.is_pressed("z"):
                if(self.verbose): print("z pressed")
                self.__keyboard_input = "Z"
            elif keyboard.is_pressed("x"):
                if(self.verbose): print("x pressed")
                self.__keyboard_input = "X"
            else:
                if(self.verbose): print("NONE")
                self.__keyboard_input = "NONE"
            # time.sleep(0.01) #sleep for 10 millis for thread optimization
            
            rate.sleep()
            # rospy.loginfo(String(self.__keyboard_input))
            pass
        keyboard.unhook_all(); print("Keyboard Unhooked!\a\a")
    
    def start(self):
        """Start Listening"""
        self.__listener_thread = threading.Thread(target=self.__key_listener, daemon=True)
        if not self.__listener_thread.is_alive():
             self.__listener_thread.start()
             print("listener thread started...\a\a")
    
    def stop(self):
        """Stop Listening"""
        if self.__listener_thread is not None and self.__listener_thread.is_alive():
             self.__listener_thread.join()
             print("listener thread stopped...\a\a")
        
    def run(self):
        #define rate
        rate = rospy.Rate(100)
        self.start()
        while not rospy.is_shutdown():
            key = self.__keyboard_input
            if(key != None):
                if(key != "esc"):
                    self.__pub_key.publish(str(self.__keyboard_input))
                    # rospy.loginfo(self.__keyboard_input)
                else:
                    listener.stop()
            rate.sleep()
        
if __name__ == "__main__":
    try:
        listener = KeyListener()
        listener.run()
        # rospy.wait_for_shutdown()  # Wait for ROS shutdown signals
        pass
    except rospy.ROSInterruptException:
        print("\a")
        pass

'''sources
https://github.com/ros-teleop/teleop_twist_keyboard/blob/master/teleop_twist_keyboard.py
'''