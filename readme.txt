-attempt5 at modifying qianyuanliao controller for husky
-models from qiayuanliao4:
	-husky_hobbler.xacro (can hobble on the ground)
	-husky_defined1.xacro (easy to add and remove feet)
	-husky_midpoint.xacro (joints start in middle of range)
	-launch file loads husky.xacro (husky.xacro is a copy of husky_midpoint, with feet activated)
-Tests to resolve 'recalculations' error:
	-Kp 350 -> 10, Kd 37 -> 0 in task.info swingLegTask
		-ERROR
	-husky_crouching
		-change urdf so the robot starts lying on the ground (feet not needed for support)
			-chenghao's advice
			-ERROR
		-change all joint initial posiitons to avoid calculations near 0
			-change defaultJointState in reference.info
				-ERROR
			-change initialState in task.info to defaultJointState
				-ERROR
	-Husky_crouching_no_fin
		-remove fin
			-ERROR
		-add feet back
			-ERROR
		-add whole feet?
	-husky aug 15:
		adding on to chenghao's changes
		added pid for feet
		task.info changed feet friction
		task.info changed phase transisition time

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
set-title "start ctrl"
/home/franksl/qiayuanliao_ws5/src/mpc_legged_control/scripts/start_controller.py

Terminal 4:
set-title "rqt_gui"
rosrun rqt_gui rqt_gui



To close gzserver:
killall -9 gzserver



Final Changes:
-set HEIGHT to 0.42 with feet, 0.37 without feet
-husky_description created following format of legged_unitree_description
	-launch file HEIGHT
-modifications to make husky_description stand alone:
	-generate_urdf.sh from legged_common moved to husky_description (SUCCESS)
	-config file from legged_gazebo moved to husky_description (SUCCESS)
	-empty_world from legged_gazebo to husky_description (SUCCESS)
-legged_controllers config/husky
	-changed a1 references to husky
	-changed defaultJointState and legJointPositions to 0 in reference.info and task.info
	-changed comheight, p_baseZ to HEIGHT in reference.info and task.info
	-changed target Velocities in reference.info to match chenghao's values
	-changed swing_trajectory_config in task.info to match chenghao's values
	-changed DDP settings in task.info to match chenghao's values
	-changed multiple shooting sqp and ipm settings in task.info to match chenghao's values
