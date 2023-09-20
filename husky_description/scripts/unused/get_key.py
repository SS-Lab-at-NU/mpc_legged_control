#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

def getKey(settings, timeout):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

if __name__ == "__main__":
    settings = saveTerminalSettings()
    key_timeout = rospy.get_param("~key_timeout", 0.5)

    rospy.init_node('keyboard')
    pub = rospy.Publisher('keyboard/keypress', String, queue_size=10)
    rate = rospy.Rate(20)

    try:
        while not rospy.is_shutdown():
            key=getKey(settings, key_timeout)
            #rospy.loginfo(key)
            pub.publish(key)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass

'''sources
https://github.com/ros-teleop/teleop_twist_keyboard/blob/master/teleop_twist_keyboard.py
'''