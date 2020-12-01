# -*- coding: utf-8 -*-
"""
Created on Wed Nov 4 2020

Written by EJ_Chang
"""


from datetime import date
import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 

# Import setting dictionaries
from Solarized import * # Solarized color palette
from GUI_Material import * # Prototype OSD GUI
from ARDTrigger import * # Response trigger



'''
# Subject profile
'''
today = date.today()
print('Today is %s:' % today)
usernum = int(input('Please enter subject number:'))
username = input("Please enter your name:").upper()
print('Hi %s, welcome to our experiment!' % username)



# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()


# Name and assign input pins
sig_input_jx = board.get_pin('a:3:i') # joystick - sx
sig_input_jy = board.get_pin('a:5:i') # joystick - sy
sig_input_jc = board.get_pin('d:8:i') # joystick - clk

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

# my_win = visual.Window(size = (880, 440), pos = (880,800), 
#                        color = SOLARIZED['base03'], colorSpace = 'rgb255', 
#                        monitor = mon, units = 'pix', screen = 1)


my_win = visual.Window(size = (2560, 1440), pos = (0,0), 
                       color = SOLARIZED['base03'], colorSpace = 'rgb255', 
                       monitor = mon, units = 'pix', 
                       screen = 0, fullscr = 1)
# Exp starts! =======
initialTime = core.getTime()
currentTime = core.getTime()
pre_pressTime = core.getTime()
iCol = 0
iRow = 0
nRow = 4
nCol = 3
final_answer = 0
stepToGoal = 0
response = []


# Prepare mouse
mouse = event.Mouse(visible = True, win = my_win)
mouse.clickReset() # Reset to its initials


'''
Instruction
'''
IMG_START = 'Img/start.png'
IMG_THX = 'Img/thanks.png'


img = visual.ImageStim(my_win, image = IMG_START)
img.draw()
my_win.flip()
core.wait(3)


# Strat the experiment ---- 

queNum = 0

for trial in range(10):    
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

        # Trace
        if len(clue) >= 1:
            for footstep in range(len(clue)):
                traCol = clue[footstep][0]
                traRow = clue[footstep][1]

                trace = visual.Rect(my_win,
                    width = requestLUT[traCol]['width'],
                    height = requestLUT[traCol]['height'],
                    lineWidth = 2,
                    fillColor = None,
                    lineColor = '#586e75',
                    pos = requestLUT[traCol]['position'][traRow], opacity = 1)
                trace.draw()


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

        hw_required = 'Joystick'
        trigger_wait = 1

        while trigger_wait == 1:
            # Read ports of required hardware ==== 
            joy_x = sig_input_jx.read()
            joy_y = sig_input_jy.read()
            joy_c = sig_input_jc.read()
            # Get joystick function
            resp_key, trigger_wait =  getJoystickRev(joy_x, joy_y, joy_c)


            if resp_key != pre_key:
                currentTime = core.getTime()

                # Check response ===== 
                final_answer = response_check(resp_key, iRow, iCol, reqRow, reqCol)

                # UI change followed response ==== 
                iRow, iCol = determine_UI(hw_required, resp_key, iRow, iCol)

                if resp_key != 'None':
                    response.append([
                                    reqRow, reqCol,
                                    resp_key, iRow, iCol, final_answer, stepToGoal,
                                    currentTime - stimuli_time, currentTime
                                    ])

                    if final_answer == 0:
                        stepToGoal += 1
                        print(resp_key)
                        if resp_key == 'Button':
                            iRow = 0
                    elif final_answer == 1:
                        if resp_key == 'Click':
                            reqCol += 1
                            iRow = 0
                            stepToGoal = 0
                            if reqCol > nCol:
                                trialStatus = 0
                            queNum += 1
                            reqRow = PseudoRandomRow[queNum]
                        stimuli_time = core.getTime()

            pre_key = resp_key



# End
core.wait(1)
img = visual.ImageStim(my_win, image = IMG_THX)
img.draw()
my_win.flip()
core.wait(3)


# Close the window
my_win.close()


        

# Experiment record file
os.chdir('/Users/YJC/Dropbox/ExpRecord_HSI/J_1_Rev')
filename = ('%s_%s.txt' % (today, username))
filecount = 0

while os.path.isfile(filename):
    filecount += 1
    filename = ('%s_%s_%d.txt' % (today, username, filecount))


with open(filename, 'w') as filehandle: 
    for key in response:
        for item in key:
            filehandle.writelines("%s " % item)
        filehandle.writelines("\n")

        
ㄇ