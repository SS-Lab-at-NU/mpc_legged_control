changes made to stop spinning:

changed joint limits in: 
huskybeta/const.xacro
common/leg.xacro.
config/reference.info
config/task.info

made _frank and _chenghao variants
changes summarized in joint_changes file
	
To launch:
	
Terminal 1:
source ~/beta_ws/devel/setup.bash
set-title "gazebo"
export ROBOT_TYPE=huskybeta
roslaunch legged_unitree_description empty_world.launch

Terminal 2:
source ~/beta_ws/devel/setup.bash
set-title "load ctrl"
export ROBOT_TYPE=huskybeta
roslaunch legged_controllers load_controller.launch cheater:=false

reset pose

Terminal 3:
set-title "start ctrl"
/home/franksl/beta_ws/HuskyBeta_firmware/legged_control/scripts/start_controller.py

Terminal 4:
set-title "rqt_gui"
rosrun rqt_gui rqt_gui

