# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import pyfirmata
import time
import os, random, time 
from psychopy import visual, event, core, monitors 


board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()


sig_input_1 = board.get_pin('d:4:i') 

pre_stat = []
initialTime = core.getTime()
currentTime = core.getTime()


print('start!')

# while True:
while currentTime - initialTime < 20: # Wait 10 sec
    # Time
    currentTime = core.getTime()

    sw_1 = sig_input_1.read()
    
    # if sw_1 != pre_stat:
    print(sw_1)

    # pre_stat = sw_1

