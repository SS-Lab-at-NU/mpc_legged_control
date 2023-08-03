-attempt5 at modifying qianyuanliao controller for husky
-models from qiayuanliao4:
	-husky_hobbler.xacro (can hobble on the ground)
	-husky_defined1.xacro (easy to add and remove feet)
	-husky_midpoint.xacro (joints start in middle of range)
	-launch file loads husky.xacro (husky.xacro is a copy of husky_midpoint)


To launch husky_description:
	
Terminal 1:
source ~/qiayuanliao_ws5/devel/setup.bash
set-title "gazebo"
roslaunch husky_description husky_world.launch

Terminal 2:
source ~/qiayuanliao_ws5/devel/setup.bash
set-title "load ctrl"
export ROBOT_TYPE=husky
roslaunch legged_controllers load_controller.launch cheater:=false

Terminal 3:
source ~/qiayuanliao_ws5/devel/setup.bash
set-title "start ctrl"
/home/franksl/qiayuanliao_ws5/src/mpc_legged_control/scripts/start_controller.py

Terminal 4:
source ~/qiayuanliao_ws5/devel/setup.bash
set-title "rqt_gui"
rosrun rqt_gui rqt_gui



To close gzserver:
killall -9 gzserver


Changes:
-husky_description created following format of legged_unitree_description
-modifications to make husky_description stand alone:
	-generate_urdf.sh from legged_common moved to husky_description (SUCCESS)
	-config file from legged_gazebo moved to husky_description (SUCCESS)
	-empty_world from legged_gazebo to husky_description (SUCCESS)
-legged_controllers config/husky
	-changed a1 references to husky
	-changed defaultJointState and legJointPositions to 0 in reference.info and task.info
	-changed comheight, p_baseZ to 0.37 in reference.info and task.info
	-changed target Velocities in reference.info to match chenghao's values
	-changed swing_trajectory_config in task.info to match chenghao's values
	-changed DDP settings in task.info to match chenghao's values
	-changed multiple shooting sqp and ipm settings in task.info to match chenghao's values
	-LOOK AT KP AND KD in swinglegtask
