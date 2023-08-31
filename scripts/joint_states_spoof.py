#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState

class joint_states_spoof(object):
    def __init__(self):
        #Node
        rospy.init_node('joint_states_spoof',anonymous=False)
        
        #Publishers
        self.pub = rospy.Publisher('/joint_states', JointState, queue_size=10)

        #Subscriber
        sub = rospy.Subscriber("/pre_joint_states", JointState, self.listen)

        #Variables
        self.pre_joint_states = JointState()

        self.parent_names = ["RF_KFE","LF_KFE","LH_KFE","RH_KFE"]
        self.child_names1 = ["RF_ankle","LF_ankle","LH_ankle","RH_ankle"]
        self.child_names2 = ["fr_control_rod","fl_control_rod","bl_control_rod","br_control_rod"]

        self.test = ""

    def listen(self, data):
        self.pre_joint_states = data
        #rospy.loginfo(data)

    def run(self):
        #define rate
        rate = rospy.Rate(100)

        while not rospy.is_shutdown():
            joint_states = self.pre_joint_states

            parent_index = ['']*4
            child_index1 = ['']*4
            child_index2 = ['']*4

            try:
                for i in range(4):
                    parent_index[i] = joint_states.name.index(self.parent_names[i])
                    child_index1[i] = joint_states.name.index(self.child_names1[i])
                    child_index2[i] = joint_states.name.index(self.child_names2[i])
                    
                for i in range(4):
                    joint_states.position = joint_states.position[1:parent_index[i]-1]+\
                        joint_states.position[parent_index[i]]+\
                        joint_states.position[parent_index[i]+1:len(joint_states.position)-1]
            
            except ValueError:
                pass

            self.pub.publish(joint_states)

            rate.sleep()
    
if __name__ == '__main__':
    try:
        spoof_node = joint_states_spoof()
        spoof_node.run()
    except rospy.ROSInterruptException:
        pass