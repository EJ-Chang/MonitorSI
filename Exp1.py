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
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_jx = board.get_pin('a:3:i') # joystick - sx
sig_input_jy = board.get_pin('a:5:i') # joystick - sy
sig_input_jc = board.get_pin('d:8:i') # joystick - clk
sig_input_dc = board.get_pin('d:12:i') # dial - sw
sig_input_dx = board.get_pin('d:11:i') # dial - dt
sig_input_dy = board.get_pin('d:10:i') # dial - clk
sig_input_bt = board.get_pin('d:9:i') # Omron

# Initial status of input pins

# Set initial values
pre_stat = []
log = []
resp_status = 0
trigger = []
pre_resp_status = []
pre_click = []
pre_button = []
resp_key = []
clue = []
pre_key = []
pre_port = []
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
pre_pressTime = core.getTime()
iCol = 0
iRow = 0
nRow = 4
nCol = 3

stepToGoal = 0
response = []

# while currentTime - initialTime < 20: # Wait 10 sec
#     # Time
#     currentTime = core.getTime()


# Strat the experiment ---- 

queNum = 0

for trial in range(1):    
    # Initial values for every trial
    trialStatus = 1
    iRow = 0
    iCol = 0
    reqCol = 0
    # reqRow = random.randrange(1, nRow + 1)
    reqRow = PseudoRandomRow[queNum]
    stimuli_time = core.getTime()
    currentTime = core.getTime()
    # print(trial)

    while trialStatus == 1:
        # Background OSD
        for image in range(5):
            img = visual.ImageStim(my_win,
                image = imageLUT[image]['path'],
                pos = imageLUT[image]['position'])
            img.draw()

        # Request
        request = visual.Rect(my_win,
            width = requestLUT[reqCol]['width'],
            height = requestLUT[reqCol]['height'],
            lineWidth = 2,
            fillColor = None,
            lineColor = '#b58900',
            pos= requestLUT[reqCol]['position'][reqRow], opacity = 1)
        request.draw()

        # Indicator
        indicator = visual.Rect(my_win, 
            width = indicatorLUT[iCol]['width'], 
            height = indicatorLUT[iCol]['height'], 
            fillColor = SOLARIZED['cyan'], fillColorSpace='rgb255', 
            lineColor = SOLARIZED['cyan'], lineColorSpace ='rgb255', 
            pos= indicatorLUT[iCol]['position'][iRow], opacity = 0.5)
        indicator.draw()

        # OSD strings
        for image in range(iCol+1):
            img = visual.ImageStim(my_win,
                image = strLUT[image]['path'],
                pos = strLUT[image]['position'])
            img.draw()

        my_win.flip()

        flipTime = core.getTime()
    # ===== End of drawing UI ====

    # ==== Wait for response ====
        '''
        HW
        '''
        # hw_required = 'Dial'
        hw_required = 'Joystick'
        trigger_wait = 1
        while trigger_wait == 1:
            # Read ports of required hardware ==== 
            if hw_required == 'Joystick':
                joy_x = sig_input_jx.read()
                joy_y = sig_input_jy.read()
                joy_c = sig_input_jc.read()
                # Get joystick function
                resp_key, trigger_wait =  getJoystick(joy_x, joy_y, joy_c)

                # if [joy_x, joy_y, joy_c] != pre_port:
                if resp_key != pre_key:
                    currentTime = core.getTime()
                    if currentTime - pre_pressTime > 0.01:
                    # print(currentTime - pre_pressTime)
                        # Check response ===== 
                        final_answer = response_check(resp_key, iRow, iCol, reqRow, reqCol)

                        # UI change followed response ==== 
                        iRow, iCol = determine_UI(hw_required, resp_key, iRow, iCol)
                        # Get action time
                        pre_pressTime = currentTime
                    else:
                        trigger_wait = 0

                # pre_port = [joy_x, joy_y, joy_c]
                pre_key = resp_key


            elif hw_required == 'Dial':
                dial_c = sig_input_dc.read()
                dial_x = sig_input_dx.read()
                dial_y = sig_input_dy.read()
                dial_b = sig_input_bt.read()
                # Get dial function
                resp_key, resp_status, trigger_wait, trigger = getDial(dial_c, dial_x, dial_y, dial_b,
                                                                        pre_resp_status, trigger, resp_status)
                pre_resp_status = resp_status
                # print(trigger_wait)


                if [dial_c, dial_x, dial_y, dial_b] != pre_port:
                    currentTime = core.getTime()
                    if currentTime - pre_pressTime > 0.01:
                    # print(currentTime - pre_pressTime)
                        # Check response ===== 
                        final_answer = response_check(resp_key, iRow, iCol, reqRow, reqCol)

                        # UI change followed response ==== 
                        iRow, iCol = determine_UI(hw_required, resp_key, iRow, iCol)
                        # Get action time
                        pre_pressTime = currentTime
                    else:
                        trigger_wait = 0

                pre_port = [dial_c, dial_x, dial_y, dial_b]
            # pre_key = resp_key
            


        '''
        Already got trigger info
        # '''

        # # if resp_key != pre_key:
        # currentTime = core.getTime()

        # # Check response ===== 
        # final_answer = response_check(resp_key, iRow, iCol, reqRow, reqCol)

        # # UI change followed response ==== 
        # iRow, iCol = determine_UI(hw_required, resp_key, iRow, iCol)

        if resp_key != 'None':
            # print(resp_key, iRow, iCol)
            response.append([
                            reqRow, reqCol,
                            resp_key, iRow, iCol, final_answer, stepToGoal,
                            currentTime - stimuli_time, currentTime
                            ])


        if final_answer == 0:
            stepToGoal += 1
            if resp_key == 'Button':
                iRow = 0
        elif final_answer == 1:
            if resp_key == 'Click':
                # clue.append([reqCol, reqRow])
                reqCol += 1
                iRow = 0
                stepToGoal = 0
                if reqCol > nCol:
                    trialStatus = 0
                # reqRow = random.randrange(1, nRow + 1)
                queNum += 1
                reqRow = PseudoRandomRow[queNum]
                # stimuli_time = core.getTime()

    # else:
    #     pass

        


# Close the window
my_win.close()




# Experiment record file
os.chdir('/Users/YJC/Dropbox/ExpRecord_HSI')
# filename = ('%s_%s.txt' % (today, username))
filename = ('TestRecord.txt')
filecount = 0

# while os.path.isfile(filename):
#     filecount += 1
#     filename = ('%s_%s_%d.txt' % (today, username, filecount))


with open(filename, 'w') as filehandle: 
    for key in response:
        for item in key:
            filehandle.writelines("%s " % item)
        filehandle.writelines("\n")


