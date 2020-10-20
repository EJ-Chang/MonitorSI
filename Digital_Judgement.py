# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import pyfirmata
import time
import os, random, time 
from psychopy import visual, event, core, monitors 

# Preparation
board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

# Set input ports
sig_input_1 = board.get_pin('d:3:i') # sw
sig_input_3 = board.get_pin('d:5:i') # dt
sig_input_5 = board.get_pin('d:7:i') # click

# Set initial values
pre_stat = []
log = []
initialTime = core.getTime()
currentTime = core.getTime()
resp_status = 0
trigger = []
pre_resp_status = []
# Start !
print('start!')

trial_on_time = 1

# while True:
while currentTime - initialTime < 6 or trial_on_time == 1: # Wait 6 sec

    currentTime = core.getTime() # Time

    # Read ports
    sw_1 = sig_input_1.read()
    sw_3 = sig_input_3.read()
    sw_5 = sig_input_5.read()

    # Click status info
    click_stat = sw_1
    if click_stat == False:
        trial_on_time = 0
        print('end')
    # Rotation position info
    rotation_pos = [sw_3, sw_5] # rotation x,y

    # Clockwise / counter-clockwise
    if rotation_pos == [True, True]:
        resp_status = 1
        
        if len(trigger) >= 2:
            if trigger[-1] - trigger[0] < 0:
                print('Clockwise >>>')
                # log.append('Clockwise >>>')
            elif trigger[-1] - trigger[0] > 0:
                print('<<< Counter-Clockwise')
                # log.append('<<< Counter-Clockwise')
            else:
                pass
        else:
            pass        

        trigger = []

    elif rotation_pos == [False, True]:
        resp_status = 2
        if resp_status != pre_resp_status:
            trigger.append(resp_status)

    elif rotation_pos == [False, False]:
        resp_status = 3
        if resp_status != pre_resp_status:
            trigger.append(resp_status)

    elif rotation_pos == [True, False]:
        resp_status = 4
        if resp_status != pre_resp_status:
            trigger.append(resp_status)
    else:
        pass


    pre_stat = [sw_3, sw_5]
    pre_resp_status = resp_status

# Save log file
with open('rotation_log.txt', 'w') as filehandle: 
    for key in log:
        filehandle.writelines("%s " % key)
        filehandle.writelines("\n")