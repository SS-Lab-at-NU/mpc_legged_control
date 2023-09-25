#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped

def move_to_goal():
    # Initialize the ROS node
    rospy.init_node('move_to_goal_node')

    # Create a publisher for the goal
    goal_publisher = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    # Wait for the publisher to connect
    rospy.loginfo("Waiting for /move_base_simple/goal publisher to connect...")
    rospy.wait_for_message('/move_base_simple/goal', PoseStamped)

    # Create a PoseStamped message for the goal
    goal_msg = PoseStamped()
    goal_msg.header.frame_id = "world"  # Specify the reference frame (e.g., "map")
    goal_msg.pose.position.x = 10.0    # Set the X coordinate of the goal
    goal_msg.pose.position.y = 0.0     # Set the Y coordinate of the goal
    goal_msg.pose.orientation.w = 1.0  # Set the orientation (quaternion) for the goal

    # Publish the goal
    rospy.loginfo("Publishing goal to move the robot to (x=10, y=0)...")
    goal_publisher.publish(goal_msg)

    # Sleep briefly to allow time for the goal to be processed
    rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        move_to_goal()
    except rospy.ROSInterruptException:
        pass
