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


sig_input_1 = board.get_pin('a:5:i') # y
# sig_input_2 = board.get_pin('d:4:i')
sig_input_3 = board.get_pin('a:3:i') # x
# sig_input_4 = board.get_pin('d:6:i')
sig_input_5 = board.get_pin('d:7:i') # click
 
print('start!')


initialTime = core.getTime()
currentTime = core.getTime()

# while True:
while currentTime - initialTime < 10: # Wait 10 sec
    
    currentTime = core.getTime()

    sw_1 = sig_input_1.read()
    sw_3 = sig_input_3.read()
    sw_5 = sig_input_5.read()

    print(sw_1, sw_3, sw_5)