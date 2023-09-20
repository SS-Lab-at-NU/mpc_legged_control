-husky8, husky7 with better control
	keyboard
		position_control.py and keyboard_control.py are now nodes in husky_description
		keyboard_control.py has been updated with aidan's code
	ardupilot file change test (NOT EFFECTIVE)
		ardupilot/tools/autotest
			pysim/vehicleinfo.py
			default_params/copter-husky.parm
			default_params/gazebo-iris-husky.parm
	ardupilot param change (EFFECTIVE)
		param show AHRS_EKF_TYPE
		param set AHRS_EKF_TYPE 10


To launch husky_description:
	
Terminal 1:
source ~/qiayuanliao_ws8/devel/setup.bash
set-title "gazebo"
roslaunch husky_description husky_world.launch

Terminal 2:
source ~/qiayuanliao_ws8/devel/setup.bash
set-title "load ctrl"
export ROBOT_TYPE=husky
roslaunch legged_controllers load_controller.launch cheater:=false

Terminal 3:
set-title "get key"
sudo su

source /opt/ros/noetic/setup.bash
source /home/franksl/qiayuanliao_ws8/devel/setup.bash
cd /home/franksl/qiayuanliao_ws8/src/mpc_legged_control/scripts/
./aidan_get_key.py

unpause gazebo

Terminal 4:
set-title "arducopter"
cd ~/ardupilot/ArduCopter/
../Tools/autotest/sim_vehicle.py -f gazebo-iris --console

Terminal 5:
set-title "rqt_gui"
rosrun rqt_gui rqt_gui


Arducopter Notes:

launch iris description:
gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_runway.world

on first use:
param set AHRS_EKF_TYPE 10

mode GUIDED
arm throttle
takeoff 2
position x y z
attitude q0 q1 q2 q3 thrust 
mode Land / RTL


Test ocs2 copter:
source ~/qiayuanliao_ws8/devel/setup.bash
set-title "test"
roslaunch ocs2_quadrotor_ros	quadrotor.launch


Keyboard controller:
Press Z to turn off position controller, turn on wbc
Press X to turn off wbc, turn on position controller
WASD to navigate


To close gzserver:
killall -9 gzserver
