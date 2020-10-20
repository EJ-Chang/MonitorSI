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


sig_input_1 = board.get_pin('d:3:i') # sw
# sig_input_2 = board.get_pin('d:4:i')
sig_input_3 = board.get_pin('d:5:i') # dt
# sig_input_4 = board.get_pin('d:6:i')
sig_input_5 = board.get_pin('d:7:i') # click
 

resp_meaning = ['Up ^', 'Click .', 'Left <', 'Down V', 'Right >']
pre_stat = []
log = []
initialTime = core.getTime()
currentTime = core.getTime()
resp = 0

print('start!')

# while True:
while currentTime - initialTime < 6: # Wait 10 sec
    # Time
    currentTime = core.getTime()


    sw_1 = sig_input_1.read()
    sw_3 = sig_input_3.read()
    sw_5 = sig_input_5.read()

    current_stat = [sw_1, sw_3, sw_5]  

    # if pre_stat = [True, True, True]:
    #     SAVE_1H_PHASE = True
        
    #     if SAVE_1H_PHASE  == True:
    #         if current_stat != [True, False, False]:
    #             half_phase_1 = current_stat
    #         else:
    #             pass
    #             print('Lack of 1H phase info!')

    if current_stat == [True, True, True]:
        resp = '-----'
        if resp != pre_resp:
            log.append(resp)
    elif current_stat == [True, False, True]:
        resp = 2
        if resp != pre_resp:
            log.append(resp)
    elif current_stat == [True, False, False]:
        resp = 3
        if resp != pre_resp:
            log.append(resp)
    elif current_stat == [True, True, False]:
        resp = 4
        if resp != pre_resp:
            log.append(resp)
    else:
        pass

    pre_stat = [sw_1, sw_3, sw_5]
    pre_resp = resp


with open('digitalInput_log.txt', 'w') as filehandle: 
    for key in log:
        filehandle.writelines("%s " % key)
        filehandle.writelines("\n")