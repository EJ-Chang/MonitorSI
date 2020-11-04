# -*- coding: utf-8 -*-
"""
Created on Wed Nov 4 2020

Written by EJ_Chang
"""

import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 

# Import setting dictionaries
from Solarized import * # Solarized color palette
from GUI_Material import * # Prototype OSD GUI
from ARDTrigger import * # Response trigger


# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_jx = board.get_pin('a:1:i') # joystick - x
sig_input_jy = board.get_pin('a:2:i') # joystick - y
sig_input_jc = board.get_pin('d:3:i') # joystick - click
sig_input_sw = board.get_pin('d:5:i') # dial - sw
sig_input_dt = board.get_pin('d:6:i') # dial - dt
sig_input_cl = board.get_pin('d:7:i') # dial - click
sig_input_om = board.get_pin('d:10:i') # Omron

# Initial status of input pins

# Set initial values
pre_stat = []
log = []
resp_status = 0
trigger = []
pre_resp_status = []
pre_click = []
pre_button = []
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



# Exp starts! =======
initialTime = core.getTime()
currentTime = core.getTime()
clickTime = core.getTime()
buttonTime = core.getTime()
iCol = 0
iRow = 0
pre_buttonTime = buttonTime
pre_clickTime = clickTime

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
    # ===== End of drawing UI ====

    # ==== Wait for response ====
    trigger_wait = 1

    while trigger_wait == 1:
        # Read ports
        tg_jx = sig_input_jx.read()
        tg_jy = sig_input_jy.read()
        tg_jc = sig_input_jc.read()
        tg_sw = sig_input_sw.read()
        tg_dt = sig_input_dt.read()
        tg_cl = sig_input_cl.read()
        tg_om = sig_input_om.read()

        # Collect as a list
        joystick = [tg_jx, tg_jy, tg_jc]
        dial = [tg_sw, tg_dt, tg_cl, tg_om]

        # Get response
        # response_hw, response_key, response_status = getAnything(mouse, joy)
        response_hw, response_key, response_status =  getPorts(joystick, dial)


# Close the window
my_win.close()