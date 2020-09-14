# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2020

Written by EJ_Chang
"""

import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 

# Import setting dictionaries
from Solarized import * # Solarized color palette
from GUI_Material import * # Prototype OSD GUI


# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_3 = board.get_pin('d:3:i')
sig_input_5 = board.get_pin('d:5:i')
sig_input_7 = board.get_pin('d:7:i')

# Initial status of input pins
pre_stat = [0, 0, 0]

'''

Create prototype OSD interface

'''
# Make screen profile ----
widthPix = 2560 # screen width in px
heightPix = 1440 # screen height in px
monitorwidth = 60 # monitor width in cm
viewdist = 60 # viewing distance in cm
monitorname = 'ProArt27'
scrn = 0 # 0 to use main screen, 1 to use external screen
mon = monitors.Monitor(monitorname, width = monitorwidth, distance = viewdist)
mon.setSizePix((widthPix, heightPix))
mon.save()

# Preparing Window ----

my_win = visual.Window(size = (880, 440), pos = (880,1040), 
                       color = SOLARIZED['base03'], colorSpace = 'rgb255', 
                       monitor = mon, units = 'pix', screen = 1)

# my_win = visual.Window(size = (2560, 1440), pos = (0,0), 
#                        color = SOLARIZED['base03'], colorSpace = 'rgb255', 
#                        monitor = mon, units = 'pix', 
#                        screen = 0, fullscr = 1)


# Exp starts! =======
initialTime = core.getTime()
currentTime = core.getTime()
iCol = 0
iRow = 0

while currentTime - initialTime < 30: # Wait 10 sec
    # Time
    currentTime = core.getTime()

    # Background OSD
    for image in range(5):
        img = visual.ImageStim(my_win,
            image = imageLUT[image]['path'],
            pos = imageLUT[image]['position'])
        img.draw()

    # OSD strings
    for image in range(4):
        img = visual.ImageStim(my_win,
            image = strLUT[image]['path'],
            pos = strLUT[image]['position'])
        img.draw()

    # Indicator
    indicator = visual.Rect(my_win, 
        width = indicatorLUT[iCol]['width'], 
        height = indicatorLUT[iCol]['height'], 
        fillColor = SOLARIZED['yellow'], fillColorSpace='rgb255', 
        lineColor = SOLARIZED['yellow'], lineColorSpace ='rgb255', 
        pos= indicatorLUT[iCol]['position'][iRow], opacity = 0.8)

    indicator.draw()


    my_win.flip()
    flipTime = core.getTime()

    triggerWait = 1

    while triggerWait == 1:
        # Collect input within a while loop
        input_c = sig_input_3.read() # click
        input_x = sig_input_5.read() # X
        input_y = sig_input_7.read() # Y


        if [input_c, input_x, input_y] != pre_stat:
            # print(input_c, input_x, input_y)
            # print('---')
            
            if [input_c, input_x, input_y] == [1, 1, 1]:
                print('---')

                if pre_stat[0] == 0:
                    iRow += 1
                    if iRow >=4: 
                        iRow == 4
                    print('next', iRow)

                    triggerWait = 0
                elif pre_stat[1] == 0 and pre_stat[2] == 0:
                    print('pass', iCol)
                    pass
                elif pre_stat[1] == 1 and pre_stat[2] == 0: # Counter-clockwise
                    iCol -= 1
                    if iCol < 0:
                        iCol = 0
                    print('counter-clockwise', iCol)
                    triggerWait = 0

                elif pre_stat[1] == 0 and pre_stat[2] == 1: # Clockwise
                    iCol += 1
                    if iCol >= 3:
                        iCol = 3
                    print('clockwise', iCol)
                    triggerWait = 0



        pre_stat = [input_c, input_x, input_y]



# Close the window
my_win.close()