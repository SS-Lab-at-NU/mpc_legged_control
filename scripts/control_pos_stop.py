#!/usr/bin/env python3

import rosservice
import time

if __name__ == '__main__':
    time.sleep(1)
    rosservice.call_service("/husky/controller_manager/switch_controller",[[''],\
        ['joint_state_controller',\
        'fr_hip_frontal_position_controller','fr_hip_sagittal_position_controller','fr_knee_position_controller',\
        'br_hip_frontal_position_controller','br_hip_sagittal_position_controller','br_knee_position_controller',\
        'fl_hip_frontal_position_controller','fl_hip_sagittal_position_controller','fl_knee_position_controller',\
        'bl_hip_frontal_position_controller','bl_hip_sagittal_position_controller','bl_knee_position_controller',\
        ],0,False, 0.0])