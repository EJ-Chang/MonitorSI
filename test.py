# -*- coding: utf-8 -*-


import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 


# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_3 = board.get_pin('d:10:i')
sig_input_5 = board.get_pin('d:11:i')
sig_input_7 = board.get_pin('d:12:i')
i = 1

while i < 200:

    # Collect input within a while loop
    input_x = sig_input_3.read() # 
    input_y = sig_input_5.read() # X
    input_c = sig_input_7.read() # Y

    # i += 1
    print(input_x,input_y,input_c)