# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

while True:
    board.digital[13].write(1) #On 5V
    time.sleep(1) # for 1 second
    board.digital[13].write(0) #Off 0V
    time.sleep(1) # for 1 second



