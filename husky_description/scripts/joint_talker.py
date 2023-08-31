#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState


def fr_hip_frontal_cmd(position: float = 0.0):
    pub = rospy.Publisher('/husky/fr_hip_frontal_position_controller/command', Float64, queue_size=10)
    rospy.init_node('fr_hip_frontal_cmd',anonymous=True)
    rate = rospy.Rate(20)
    i=0
    while not rospy.is_shutdown():
        #rospy.loginfo(position)
        pub.publish(position)
        rate.sleep()
        i+=1
        
if __name__ == '__main__':
    try:
        fr_hip_frontal_cmd(0.5)
    except rospy.ROSInterruptException:
        pass
    
'''sources
https://www.youtube.com/watch?v=3C_F8vhnUPI
https://stackoverflow.com/questions/2489669/how-do-python-functions-handle-the-types-of-parameters-that-you-pass-in
'''