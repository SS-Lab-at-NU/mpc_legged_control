#!/usr/bin/env python3

import rosservice
import time

name = ["RF_HAA", "RF_HAE", "RF_KFE", \
        "LF_HAA", "LF_HAE", "LF_KFE", \
        "LH_HAA", "LH_HAE", "LH_KFE", \
        "RH_HAA", "RH_HAE", "RH_KFE",]

position = [0, 0, 0, 0, \
            0, 0, 0, 0, \
            0, 0, 0, 0, \
            0, 0, 0, 0]

if __name__ == '__main__':
    time.sleep(1)
    #rosservice.call_service("/gazebo/unpause_physics",[])
    #time.sleep(.01)
    rosservice.call_service("/gazebo/set_model_configuration",\
    ['husky','legged_robot_description',name,position])
    #time.sleep(.02)
    #rosservice.call_service("/gazebo/pause_physics",[])