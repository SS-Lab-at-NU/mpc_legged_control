-husky7, same as husky5 but with some tweaks
	trying to make the stance controllable by keyboard
		changes to ocs2_robotic_examples/ocs2_legged_robot_ros/src/gait
	trying to fix an rviz display error, mimic joints not updating
		attempt did not work
		added rviz publishers to launch file
		created joint spoofer in scripts, did not work
		implemented hussain's joint spoofer (temporarily paused)
	ardupilot
		implemented, and implemented switching as per below


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
set-title "arducopter"
cd ~/ardupilot/ArduCopter/
../Tools/autotest/sim_vehicle.py -f gazebo-iris --console

Terminal 3:
set-title "stop pos"
cd
cd qiayuanliao_ws7/src/mpc_legged_control/scripts
./control_pos_stop.py

Terminal 4:
set-title "start wbc"
cd qiayuanliao_ws7/src/mpc_legged_control/scripts
./control_wbc_start.py

Terminal 5:
set-title "rqt_gui"
rosrun rqt_gui rqt_gui

Terminal 6:
set-title "keyboard"
/home/franksl/qiayuanliao_ws7/src/mpc_legged_control/scripts/keyboard_control.py


Arducopter Notes:

launch iris description:
gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_runway.world

mode GUIDED
arm throttle
takeoff 2


To close gzserver:
killall -9 gzserver


Sources:
https://github.com/ArduPilot/ardupilot_gazebo
https://github.com/SS-Lab-at-NU/m4_simulation
https://github.com/Intelligent-Quads/iq_tutorials/blob/master/docs/installing_gazebo_arduplugin.md
https://www.youtube.com/watch?v=m7hPyJJmWmU


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
