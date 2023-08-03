-attempt4 at modifying qianyuanliang workshet. i will take the working model and try to break it
-will try launching a1_consolidated to see if separate xacro files are necessary - SUCCESS
-will try launching husky_one_to_one (husky with joints renamed and base removed) - failure (mesh error)
	-will use absolute reference instead of relative - SUCCESS (new error, imu not found)
	-updated IMU definition in husky xacro - failure (same error)
	-changed husky name to 'a1' - failure (same error)
	-see legged_gazebo/LeggedHWSim
-launch husky from within unitree_description
	-it loads, but flies off into space (max num of working set recalcs performed)
	-put back mirror joints - (same error, husky_error1)
	-changed thigh inertias, simplified collisions (same error)
	-add mu kp kd selfCollide as per robot_a1 (same error)
	-change config file default position (same error)
	-make chenghao's changes to ref and task.info files re thread count etc (same error)
	-add a dummy link for the body to add inertia (inconclusive)
	-change joint damping friction effort to match unitree a1 (it fails, but not as much)
	-make ankle revolute to fix mimic (husky_error2)
	-reduce 'foot_fixed' link to only a sphere (husky_error3)
	-husky with nub feet (it kind of hobbles, husky_hobbler)
	-simplify more (no effect)
		-disable fixed joint lumping for feet
		-simplify base
	-husky with rotation directions reversed (inconclusive, husky_error4)
		right reverse
		left reverse
		both reverse
	-put back foot (husky_error5)
	-created flexible urdf with well defined foot / nub / control rod sections (husky_defined1)
	-remove foot, reverse direction of right joints
	-set initial position of all joints in midpoint of rotation range



To launch:
	
Terminal 1:
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "gazebo"
export ROBOT_TYPE=a1
roslaunch legged_unitree_description empty_world.launch

Terminal 1 (a1_c):
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "gazebo"
export ROBOT_TYPE=a1_c
roslaunch legged_unitree_description a1_c_world.launch

Terminal 1 (husky_one_to_one):
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "gazebo"
roslaunch husky_one_to_one empty_world.launch

Terminal 1 (unitree husky):
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "gazebo"
roslaunch legged_unitree_description husky_world.launch

Terminal 2:
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "load ctrl"
export ROBOT_TYPE=a1
roslaunch legged_controllers load_controller.launch cheater:=false

Terminal 2 (unitree husky):
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "load ctrl"
export ROBOT_TYPE=husky
roslaunch legged_controllers load_controller.launch cheater:=false

Terminal 3:
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "start ctrl"
/home/franksl/qiayuanliao_ws4/scripts/start_controller.py

Terminal 4:
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "rqt_gui"
rosrun rqt_gui rqt_gui

Terminal 5:
source ~/qiayuanliao_ws4/devel/setup.bash
set-title "scripts"
qiayuanliao_ws1/scripts/keyboard_control_a1.py





To close gzserver:
killall -9 gzserver


Changes made to:
legged_unitree_description husky.xacro
legged_unitree_description husky_world.launch
legged_controllers config/husky
