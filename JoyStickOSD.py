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
sig_input_x = board.get_pin('a:1:i') # x
sig_input_y = board.get_pin('a:2:i') # y
sig_input_c = board.get_pin('d:3:i') # click
 

# Initial status of input pins

# Set initial values
pre_stat = [0, 0]
sw_x = 0
sw_y = 0
trigger = 'None'
pre_trigger = 'None'
# Start !
print('start!')


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

my_win = visual.Window(size = (880, 440), pos = (880,800), 
                       color = SOLARIZED['base03'], colorSpace = 'rgb255', 
                       monitor = mon, units = 'pix', screen = 1)

# my_win = visual.Window(size = (2560, 1440), pos = (0,0), 
                       # color = SOLARIZED['base03'], colorSpace = 'rgb255', 
                       # monitor = mon, units = 'pix', 
                       # screen = 0, fullscr = 1)
# my_win = visual.Window(size = (2560, 1440), pos = (0,0), 
#                        color = SOLARIZED['base03'], colorSpace = 'rgb255', 
#                        monitor = mon, units = 'pix', 
#                        screen = 0, fullscr = 1)


# Exp starts! =======
initialTime = core.getTime()
currentTime = core.getTime()
clickTime = core.getTime()
iCol = 0
iRow = 0

while currentTime - initialTime < 20: # Wait 10 sec
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

    # Response
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
                iRow -= 1
                if iRow <= 0:
                    iRow = 0
            elif D1 < 0 and D2 > 0:
                trigger = 'Left'
                iCol -= 1
                if iCol <= 0:
                    iCol = 0
            elif D1 < 0 and D2 < 0:
                trigger = 'Down'
                iRow += 1
                if iRow >= 4:
                    iRow = 4
            elif D1 > 0 and D2 < 0:
                trigger = 'Right'
                iCol += 1
                if iCol >= 3:
                    iCol = 3
        else:
            trigger = 'None'


    if trigger != pre_trigger:
        print(trigger)
    else:
        pass

    pre_trigger = trigger


# Close the window
my_win.close()