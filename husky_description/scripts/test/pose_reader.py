#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Float64
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion

import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import subprocess
import os

class pose_reader(object):
    def __init__(self):
        #Node
        rospy.init_node('husky_pose_publisher')

        #Publishers
        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        # position_publisher = rospy.Publisher('husky_position', Point, queue_size=10)
        # yaw_publisher = rospy.Publisher('husky_yaw', Float64, queue_size=10)

        #Subscribers
        key_sub = rospy.Subscriber("/keyboard/keypress", String, self.update_key)
        pose_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_pose_callback)
        
        #Variables
        self.keyboard_input = ""
        self.cmd_vel = Twist()

        self.null_speed = 0.3
        self.forward_speed = 0.38
        self.back_speed = -0.01
        self.turn_speed = 0.5

    def update_key(self, data):
        self.keyboard_input = data

    def num_to_str(self,num):
        num = round(num, 3)

        last_decimal_place = int(num * (10**3)) % 10
        
        if last_decimal_place == 0:
            return str(num)+"0"
        else:
            return str(num)

    def model_pose_callback(self,msg):
        model_index = msg.name.index('husky')
        model_pose = msg.pose[model_index]

        # Extract X, Y, and Z position
        x = model_pose.position.x
        y = model_pose.position.y
        z = model_pose.position.z

        # Extract yaw (orientation)
        orientation = model_pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])

        # # Publish position
        # position_msg = Point(x=x, y=y, z=z)
        # position_publisher.publish(position_msg)
        
        # # Publish yaw (orientation)
        # yaw_msg = Float64(data=yaw)
        # yaw_publisher.publish(yaw_msg)

        #Print position and yaw
        print("x: "+self.num_to_str(x)+", y: "+self.num_to_str(y)+\
            ", z: "+self.num_to_str(z)+", Yaw: "+str(round(yaw/np.pi*180,1))+\
            ", Key: "+str(self.keyboard_input))

    def set_velocity(self,linear_velocity:float=1.0, angular_velocity:float=1.0):
        self.cmd_vel.linear.x = linear_velocity
        self.cmd_vel.angular.z = angular_velocity
        self.pub_cmd_vel.publish(self.cmd_vel)

    def run(self):
        key = self.keyboard_input
        
        if key == String("w"):
                self.set_velocity(self.forward_speed, 0.0)
        else:
            self.set_velocity(self.null_speed, 0.0)

        prev_key = key

        rospy.spin()


if __name__ == '__main__':
    try:
        ctrl = pose_reader()
        ctrl.run()
    except rospy.ROSInterruptException:
        pass
    