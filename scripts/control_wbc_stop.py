#!/usr/bin/env python3

import rosservice
import time

if __name__ == '__main__':
    rosservice.call_service("/controller_manager/switch_controller",\
        [[''],['controllers/legged_controller'],1,True, 0.0])