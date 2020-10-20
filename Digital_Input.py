# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import pyfirmata
import time

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

while True:

    sw_1 = sig_input_1.read()
    sw_3 = sig_input_3.read()
    sw_5 = sig_input_5.read()

    print(sw_1, sw_3, sw_5)


