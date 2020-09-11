# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 

# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_3 = board.get_pin('d:3:i')
sig_input_5 = board.get_pin('d:5:i')
sig_input_7 = board.get_pin('d:7:i')

# Initial status of input pins
pre_stat = []

# Exp starts! =======
initialTime = core.getTime()
currentTime = core.getTime()
iCol = 1
iRow = 1

while currentTime - initialTime < 10: # Wait 10 sec
    # Time
    currentTime = core.getTime()

    # Collect input within a while loop
    input_c = sig_input_3.read() # click
    input_x = sig_input_5.read() # X
    input_y = sig_input_7.read() # Y


    if [input_c, input_x, input_y] != pre_stat:
        # print(input_c, input_x, input_y)
        # print('---')
        
        if [input_c, input_x, input_y] == [1, 1, 1]:
            print('---')
            if pre_stat[1] == 0 and pre_stat[2] == 0:
                print('pass', iCol)
                pass
            elif pre_stat[1] == 1 and pre_stat[2] == 0: # Counter-clockwise
                iCol -= 1
                if iCol < 0:
                    iCol = 0
                print('counter-clockwise', iCol)

            elif pre_stat[1] == 0 and pre_stat[2] == 1: # Clockwise
                iCol += 1
                if iCol >= 4:
                    iCol = 4
                print('clockwise', iCol)


    pre_stat = [input_c, input_x, input_y]

