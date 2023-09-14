#!/usr/bin/env python3

import rosservice
import time

if __name__ == '__main__':
    time.sleep(1)
    rosservice.call_service("/controller_manager/switch_controller",\
        [[''],['controllers/legged_controller'],1,True, 0.0])