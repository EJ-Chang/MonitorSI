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
sig_input_1 = board.get_pin('d:5:i')
sig_input_3 = board.get_pin('d:6:i')
sig_input_5 = board.get_pin('d:7:i')
sig_input_7 = board.get_pin('d:10:i') # Omron

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
buttonTime = core.getTime()
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

    trigger_wait = 1

    while trigger_wait == 1:
        # Read ports
        sw_1 = sig_input_1.read()
        sw_3 = sig_input_3.read()
        sw_5 = sig_input_5.read()
        sw_7 = sig_input_7.read()

        # Click status info
        click_stat = sw_1

        if click_stat == False and pre_click == True:
            clickTime = core.getTime()
            if clickTime - pre_clickTime > 0.1:
                iCol += 1
                print('Click')
                if iCol > 3:
                    iCol = 0

            trigger_wait = 0
        else:
            pass

        pre_click = sw_1
        pre_clickTime = clickTime
            # core.quit()

        # Button(back key) status info
        button_stat = sw_7

        if button_stat == False and pre_button == True:
            buttonTime = core.getTime()
            if buttonTime - pre_buttonTime > 0.1:
                iCol -= 1
                print('Back')
                if iCol <= 0:
                    iCol = 0
            trigger_wait = 0
        else:
            pass

        pre_button = sw_7
        pre_buttonTime = buttonTime


        # Rotation position info
        rotation_pos = [sw_3, sw_5] # rotation x,y

        # Clockwise / counter-clockwise
        if rotation_pos == [True, True]:
            resp_status = 1
            
            if len(trigger) >= 2:
                if trigger[-1] - trigger[0] < 0:
                    print('Clockwise >>>')
                    iRow += 1
                    if iRow >= 4:
                        iRow = 4
                    # log.append('Clockwise >>>')
                    trigger_wait = 0
                elif trigger[-1] - trigger[0] > 0:
                    print('<<< Counter-Clockwise')
                    iRow -= 1
                    if iRow <= 0:
                        iRow = 0
                    trigger_wait = 0
                    # log.append('<<< Counter-Clockwise')
                else:
                    pass
            else:
                pass        

            trigger = []

        elif rotation_pos == [False, True]:
            resp_status = 2
            if resp_status != pre_resp_status:
                trigger.append(resp_status)

        elif rotation_pos == [False, False]:
            resp_status = 3
            if resp_status != pre_resp_status:
                trigger.append(resp_status)

        elif rotation_pos == [True, False]:
            resp_status = 4
            if resp_status != pre_resp_status:
                trigger.append(resp_status)
        else:
            pass


        pre_stat = [sw_3, sw_5]
        pre_resp_status = resp_status


# Close the window
my_win.close()