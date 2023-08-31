
#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>

void odomCallback(const nav_msgs::Odometry::ConstPtr& msg) {
    // Extract necessary data from the odometry message
    geometry_msgs::TransformStamped odom_transform;
    odom_transform.header = msg->header;
    odom_transform.header.frame_id = "world";
    odom_transform.child_frame_id = "base"; // Change this if needed
    odom_transform.transform.translation.x = msg->pose.pose.position.x;
    odom_transform.transform.translation.y = msg->pose.pose.position.y;
    odom_transform.transform.translation.z = msg->pose.pose.position.z;
    odom_transform.transform.rotation.x = msg->pose.pose.orientation.x;
    odom_transform.transform.rotation.y = msg->pose.pose.orientation.y;
    odom_transform.transform.rotation.z = msg->pose.pose.orientation.z;
    odom_transform.transform.rotation.w = msg->pose.pose.orientation.w;
    
    // Publish the odometry transform
    tf2_ros::TransformBroadcaster().sendTransform(odom_transform);
}
int main(int argc, char** argv) {
    ros::init(argc, argv, "tf_odom_publisher");
    ros::NodeHandle nh;

    tf2_ros::TransformBroadcaster tf_broadcaster;
    ros::Rate rate(1000);
    
    while(nh.ok()){
    ros::Subscriber odom_sub = nh.subscribe("/ground_truth/state", 10, odomCallback);

    ros::spin(); // Enter the ROS loop
    }
    return 0;
};