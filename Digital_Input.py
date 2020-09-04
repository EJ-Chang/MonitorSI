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

digital_input_1 = board.get_pin('d:3:i')
digital_input_3 = board.get_pin('d:7:i')
digital_input_5 = board.get_pin('d:11:i')

pre_stat = []

while True:
    sw_1 = digital_input_1.read()
    sw_3 = digital_input_3.read()
    sw_5 = digital_input_5.read()

    if [sw_1, sw_3, sw_5] != pre_stat:
        print(sw_1, sw_3, sw_5)

    pre_stat = [sw_1, sw_3, sw_5]