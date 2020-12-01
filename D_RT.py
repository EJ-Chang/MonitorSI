# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 2020

Written by EJ_Chang
"""

import os, random
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors
from datetime import date
from ARDTrigger import * # Response trigger

# Subject profile
today = date.today()
print('Today is %s:' % today)
usernum = int(input('Please enter subject number:'))
username = input("Please enter your name:").upper()
print('Hi %s, welcome to our experiment!' % username)

# Make screen profile ----
widthPix = 2560 # screen width in px
heightPix = 1440 # screen height in px
monitorwidth = 60 # monitor width in cm
viewdist = 60 # viewing distance in cm
monitorname = 'ProArt27'
scrn = 0 # 0 to use main screen, 1 to use external screen
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
mon.save()


# Load initial setting ----
# Preparing Window
# my_win = visual.Window(size=(800, 600), pos=(880,1040), monitor = mon, units = 'pix', 
#                        screen = 1)
my_win = visual.Window(size=(2560, 1440), pos=(0,0), monitor = mon, units = 'pix', 
                       screen = 0, fullscr = 1)


# Preparing Joystick & Mouse

# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_dc = board.get_pin('d:12:i') # dial - sw
sig_input_dx = board.get_pin('d:11:i') # dial - dt
sig_input_dy = board.get_pin('d:10:i') # dial - clk 
sig_input_bt = board.get_pin('d:9:i') # Omron
# - Mouse setting
mouse = event.Mouse(visible = True, win = my_win)
mouse.clickReset() # Reset to its initials


# Preparing experiment stimulus
img_start = 'Img/start.png'
img_rest = 'Img/rest.png'
img_ty = 'Img/thanks.png'
img_ins = 'Img/RT_instruction.png'
lineNumber = 1
imageLUT = [] # list of image dictionary
with open("directionArrows.txt") as f:
    for line in f:
        (number, mean, filepath) = line.split()
        sti_Dict = {
        'number': lineNumber,
        'meaning': mean,
        'path': filepath
        }
        lineNumber += 1
        imageLUT.append(sti_Dict)

# Randomizing the list
nStimulus = len(imageLUT)  # nStimulus = 4
playList = list(range(nStimulus)) * 10 # playList = [0,1,2,...nStimulus] repeats twice
nTrials = len(playList)
random.shuffle(playList) # Shuffle the playList
stimulus_seq = tuple(playList) # Make it unchangable

# Preparing experiment timer
experiment_timer = core.Clock()
experiment_timer.reset()

# Setting initial numbers
item = 0


# Set initial values
response = []
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
hw_required = 'Dial'
current_time = core.getTime()
final_anser = 0
preAnswer_time = current_time

# Start experiment ----

# Greeting page
img = visual.ImageStim(win = my_win, image = img_start, 
                       units = 'pix')
img.draw()
my_win.flip()
core.wait(2)

# Trials
for item in range(40): # should be 40


    trialStatus = 1
    while trialStatus == 1:
    # for item in range(40):
        img = visual.ImageStim(win = my_win, 
                               image = imageLUT[stimulus_seq[item]]['path'],
                               units = 'pix')
        img.draw()
        my_win.flip()
        stimuli_time =core.getTime()

        trigger_wait = 1
        # Get response
        while trigger_wait == 1:

            # Read ports of required hardware ==== 
            dial_c = sig_input_dc.read()
            dial_x = sig_input_dx.read()
            dial_y = sig_input_dy.read()
            dial_b = sig_input_bt.read()

            # Get dial function
            resp_key, resp_status, trigger_wait, trigger = getDial(dial_c, dial_x, dial_y, dial_b, 
                                                               pre_resp_status, trigger, resp_status)
            key_meaning = interpret_key(hw_required, resp_key)


            if resp_key != pre_key:
                current_time = core.getTime()
                if current_time - preAnswer_time > 0.1:

                    if key_meaning == imageLUT[stimulus_seq[item]]['meaning']:
                        final_anser = 1
                        trialStatus = 0
                    else:
                        final_anser = 0

                    # Determine response key & time
                    if key_meaning != 'None':
                        response.append([stimulus_seq[item], 
                                        key_meaning,
                                        imageLUT[stimulus_seq[item]]['meaning'],
                                        final_anser,
                                        current_time -  stimuli_time,
                                        current_time
                                        ]) # correct/not, RT, real time

                    # item += 1
                    # trialStatus = 0
                    

                

            pre_key = resp_key # Button status update
            preAnswer_time = current_time
    # Resting time between stimulus
    img = visual.ImageStim(win = my_win, image = img_rest, 
                       units = 'pix')
    img.draw()
    my_win.flip()

    # Stimulus interval
    t = 0.3 + random.randrange(2)
    core.wait(t)
    # print(t)
    stimuli_time = core.getTime()

# Thank u page
img = visual.ImageStim(win = my_win, image = img_ty, units = 'pix')
img.draw()
my_win.flip()
core.wait(2)
# Close window
my_win.close()


# Exp END ----
# print('Get your responses:', response)

# Experiment record file
os.chdir('/Users/YJC/Dropbox/ExpRecord_HSI/D_RT')
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

