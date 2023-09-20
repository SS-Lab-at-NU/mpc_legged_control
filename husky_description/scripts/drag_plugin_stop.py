import rospy
import subprocess

#path to model
model_path = "/home/franksl/qiayuanliao_ws8/src/mpc_legged_control/husky_description/urdf/husky.xacro"

# List of plugins to unload
plugins = ["rotor_0_blade_1", "rotor_0_blade_2", "rotor_1_blade_1", "rotor_1_blade_2",\
    "rotor_2_blade_1", "rotor_2_blade_2","rotor_3_blade_1", "rotor_3_blade_2" ]

# Iterate through the loaded plugins
for plugin in plugins:
    # Unload the plugin
    subprocess.call(['gz', 'dynamic_unload', model_path, '-g', plugin])

# You may need to add error handling and other logic as needed.
