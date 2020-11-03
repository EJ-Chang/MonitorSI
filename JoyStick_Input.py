# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import pyfirmata
import time
from psychopy import core

board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()


sig_input_x = board.get_pin('a:1:i') # x
sig_input_y = board.get_pin('a:2:i') # y
sig_input_c = board.get_pin('d:4:i') # click
 
print('start!')


initialTime = core.getTime()
currentTime = core.getTime()

log_x = []
log_y = []
pre_stat = [0, 0]
sw_x = 0
sw_y = 0
trigger = 'None'
pre_trigger = 'None'
# L1 = y - x
# L2 = y + x - 1
# O1 = x^2 + y^2 - r^2


# while True:
while currentTime - initialTime < 10: # Wait 10 sec
    
    currentTime = core.getTime()

    sw_x = sig_input_x.read() # x
    sw_y = sig_input_y.read() # y
    sw_c = sig_input_c.read() # click

    # print(sw_x, sw_y, sw_c)


    # Breaking point
    if sw_c == False:
        trigger = 'Click'
    elif sw_c == True :
        D1 = sw_y - sw_x
        D2 = sw_y + sw_x - 1
        O1 = (sw_x-0.5) ** 2 + (sw_y-0.5) ** 2 - 0.04 # r = 0.2

        if O1 >= 0:
            if D1 > 0 and D2 > 0:
                trigger = 'Up'
            elif D1 < 0 and D2 > 0:
                trigger = 'Left'
            elif D1 < 0 and D2 < 0:
                trigger = 'Down'
            elif D1 > 0 and D2 < 0:
                trigger = 'Right'
        else:
            trigger = 'None'


    if trigger != pre_trigger:
        print(trigger)
    else:
        pass

    pre_trigger = trigger
