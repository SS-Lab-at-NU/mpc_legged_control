-husky7, same as husky5 but with some tweaks
	changes to ocs2_robotic_examples/ocs2_legged_robot_ros/src/gait


To launch husky_description:
	
Terminal 1:
source ~/qiayuanliao_ws7/devel/setup.bash
set-title "gazebo"
roslaunch husky_description husky_world.launch

Terminal 2:
source ~/qiayuanliao_ws7/devel/setup.bash
set-title "load ctrl"
export ROBOT_TYPE=husky
roslaunch legged_controllers load_controller.launch cheater:=false

unpause gazebo

Terminal 3:
set-title "start ctrl"
/home/franksl/qiayuanliao_ws7/src/mpc_legged_control/scripts/start_controller.py

Terminal 4:
set-title "rqt_gui"
rosrun rqt_gui rqt_gui

Terminal 5:
set-title "keyboard"
/home/franksl/qiayuanliao_ws7/src/mpc_legged_control/scripts/keyboard_control.py

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
