# -*- coding: utf-8 -*-
"""
Created on Mon May 11 2020

Written by EJ_Chang
"""

import os, random
from psychopy import visual, event, core, monitors
from psychopy.hardware import joystick
from datetime import date
import numpy as np
from StiGenerator import *
from ResponseTrigger import *

# This is practice trial setting
hw_required = ['Wheel','dPad']

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

# Color Palette ----
base03 = (0,43,54)
base01 = (88,110,117)
base0 = (131,148,150)
yellow = (181,137,0)
magenta = (211,54,130)
cyan = (42,161,152)
green = (133,153,0)

# Directions ----
dir_DictList= []
with open("dir_limit.txt") as f:
    for line in f:
        (number, main_dir, ortho_dir_1, ortho_dir_2, \
         main_meaning, ortho_meaning_1, ortho_meaning_2) = line.split()

        # Write a dictionary
        sti_Dict = {
        'number': number,
        'main_dir': main_dir,
        'ortho_dir': [ortho_dir_1,ortho_dir_2],
        'main_meaning': main_meaning,
        'ortho_meaning': [ortho_meaning_1, ortho_meaning_2]
        }

        dir_DictList.append(sti_Dict)

# Preparing Window ----
# my_win = visual.Window(size=(800, 800), pos=(880,1040), 
#                        color=base03, colorSpace='rgb255', 
#                        monitor = mon, units = 'pix', 
#                        screen = 1)

my_win = visual.Window(size=(2560, 1440), pos=(0,0), 
                       color=base03, colorSpace='rgb255', 
                       monitor = mon, units = 'pix', 
                       screen = 0, fullscr = 1)



# Preparing Joystick & Mouse ----
# - Joysticks setting
joystick.backend = 'pyglet'
nJoys = joystick.getNumJoysticks() # Check if I have any joysticks
id = 0 # I'll use the first one as input
joy = joystick.Joystick(id) # ID has to be nJoys - 1
# - Mouse setting
mouse = event.Mouse(visible = True, win = my_win)
mouse.clickReset() # Reset to its initials

# Preparing pics ----
img_start = 'ACC_ImgFolder/Practice_Start.png'
img_rest = 'ACC_ImgFolder/Practice_Rest.png'
img_ty = 'ACC_ImgFolder/Practice_End.png'

img_ins1 = 'ACC_ImgFolder/Practice_Ins1.png'
img_ins2 = 'ACC_ImgFolder/Practice_Ins2.png'

practice_ins = [img_ins1, img_ins2]

instruction_dict = {
    'Wheel': 'ACC_ImgFolder/acc1.png',
    'dPad':  'ACC_ImgFolder/acc2.png'}



# Setting Constants ----
ORIGIN_POINT = (0,0)
ORIGIN = visual.Circle(my_win, units =  'pix',
                       radius = 5, pos = ORIGIN_POINT,
                       fillColor = base01, fillColorSpace = 'rgb255',
                       lineColor = base01, lineColorSpace = 'rgb255', 
                       interpolate = True)

ARROW_WING1 = np.array([-10,10])
ARROW_WING2 = np.array([-10,-10])
MINI_WING1 = np.array([-5,5])
MINI_WING2 = np.array([-5,-5])


ROTATE_0 = np.array([[1,0], [0,1]])
ROTATE_90 = np.array([[0,-1], [1,0]])
ROTATE_180 = np.array([[-1,0], [0,-1]])
ROTATE_270 = np.array([[0,1], [-1,0]])
ROTATE_NONE = np.array([[0,0], [0,0]])

LINE_UP = np.array([0,40])
LINE_DOWN = np.array([0,-40])
LINE_LEFT = np.array([-40,0])
LINE_RIGHT = np.array([40,0])
LINE_NONE = np.array([0,0])

four_vector = [LINE_UP, LINE_DOWN, LINE_LEFT, LINE_RIGHT]
four_dict = {'Up': LINE_UP,  'Down': LINE_DOWN,
             'Left': LINE_LEFT, 'Right': LINE_RIGHT, 'NoMeaning': LINE_NONE}

response = []
# ===========================

# Welcoming
img = visual.ImageStim(win = my_win, image = img_start, 
                       units = 'pix')
img.draw()
my_win.flip()
core.wait(2)
# Resting 
rest = visual.ImageStim(win = my_win, image = img_rest, 
                       units = 'pix')

# Instruction
for ins in range(2):
    core.wait(0.5)
    while 1:
        img = visual.ImageStim(win = my_win, image = practice_ins[ins], 
                                 units = 'pix')
        img.draw()
        my_win.flip()
        # Get response 
        response_hw, response_key, response_status = getAnything(mouse, joy)
        if response_status == 1:
            break


# Make 2 blocks
for block in range(2):
    img = visual.ImageStim(win = my_win, image = instruction_dict[hw_required[block]], 
                           units = 'pix')
    img.draw()
    my_win.flip()
    core.wait(2)

    for nTrial in range(2):

        # Get the ques
        tag_que = [] 
        line_pos = ORIGIN_POINT
        sti_path = [ORIGIN_POINT, ORIGIN_POINT] 
        thePath = pathGenerate(dir_DictList)

        for ques in thePath:
            ques = int(ques)
            line_pos = line_pos + four_vector[ques]
            sti_path.append(line_pos) # Coordinates
            tag_que.append(dir_DictList[ques]['main_meaning'])

        N_LINE = len(tag_que)

        # Rotate along with the last line in this path
        rotation_dict = {'Up':ROTATE_270, 'Down':ROTATE_90, 
                         'Left':ROTATE_180, 'Right':ROTATE_0, 
                         'NoMeaning': ROTATE_NONE}


        # =========================
        #  Trial start !
        # =========================
        loopStatus = 1
        iResp = 0
        resp_path = [ORIGIN_POINT, ORIGIN_POINT]
        key_meaning = 'NoMeaning'
        preAnswer_time = core.getTime()
        while loopStatus == 1 :

            '''
            Stimuli routine
            '''
            # Origin point
            ORIGIN.draw()

            # Stimuli path
            for iLine in range(N_LINE):

                # Que path (stimuli) ----
                stimuli_path = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3, 
                               lineColor = base01, lineColorSpace = 'rgb255', 
                               vertices = (sti_path[iLine+1], sti_path[iLine+2]),
                               closeShape = False, pos = (0, 0))
                stimuli_path.draw()

            # End point
            end = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3, 
                  lineColor = base01, lineColorSpace = 'rgb255', 
                  vertices = (sti_path[-1] + np.dot(ARROW_WING1, 
                                                    rotation_dict[tag_que[-1]]), 
                              sti_path[-1], 
                              sti_path[-1] + np.dot(ARROW_WING2, 
                                                    rotation_dict[tag_que[-1]])),
                  closeShape = False, pos = (0, 0))
            end.draw()

            # Response path 
            for iResp in range(len(resp_path)-1):
                response_path = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3, 
                                lineColor = green, lineColorSpace = 'rgb255', 
                                vertices = (sti_path[iResp], sti_path[iResp+1]),
                                closeShape = False, pos = (0, 0))
                response_path.draw()


            # Indicator
            indicator_pos = resp_path[iResp+1]
            indicator_point = visual.Circle(my_win, units =  'pix',
                              radius = 4, pos = (indicator_pos),
                              fillColor = yellow, fillColorSpace = 'rgb255',
                              lineColor = yellow, lineColorSpace = 'rgb255', 
                              interpolate = True)
            indicator_point.draw()


            indicator_spine = indicator_pos + four_dict[key_meaning]

            indicator_line = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3,
                             lineColor = magenta, lineColorSpace = 'rgb255',
                             vertices = (indicator_pos, indicator_spine),
                             closeShape = False, pos = (0,0))
            indicator_line.draw()

            indicator_arrow = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3,
                              lineColor = magenta, lineColorSpace = 'rgb255',
                              vertices = (indicator_spine
                                          + np.dot(MINI_WING1, 
                                                   rotation_dict[key_meaning]),
                                          indicator_spine,
                                          indicator_spine
                                          + np.dot(MINI_WING2, 
                                                   rotation_dict[key_meaning])),
                              closeShape = False, pos = (0,0))
            # indicator_arrow.draw()

            

            # Flip the window
            my_win.flip()


            '''
            Response routine
            '''

            # Get response 
            response_hw, response_key, response_status = getAnything(mouse, joy)
            
            
            # if response_status == 1 and response_key != pre_key:
            if response_status == 1 and pre_status == 0:
                # Get current time
                # print(iResp, N_LINE)
                current_time = core.getTime()
                
                key_meaning = interpret_key_ACC(response_hw, response_key) 
                finalanswer = reponse_checker_ACC(response_hw, key_meaning, 
                                                  hw_required[block], tag_que[iResp])
                # Collect response (data)
                response.append([hw_required[block], nTrial, iResp, 
                    response_hw, response_key, key_meaning,
                    tag_que[iResp], finalanswer,
                    current_time - preAnswer_time, current_time
                    ]) # correct/not, RT, real time

                if finalanswer == 1:
                    key_meaning = 'NoMeaning' # Reset key meaning
                    resp_path.append(sti_path[iResp+2])
                    iResp += 1
                    if iResp >= N_LINE:
                        iResp = N_LINE

                        for iResp in range(len(resp_path)-1):
                            response_path = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3, 
                                            lineColor = green, lineColorSpace = 'rgb255', 
                                            vertices = (sti_path[iResp], sti_path[iResp+1]),
                                            closeShape = False, pos = (0, 0))
                            response_path.draw()
                        ORIGIN.draw()
                        end.draw()
                        my_win.flip()
                        core.wait(0.5)
                        loopStatus = 0
                        rest.draw()
                        core.wait(2)


                elif key_meaning == 'Abort':
                    core.quit()

                # print(key_meaning)
                # print('resp_path length:', len(resp_path))
                # print('iResp:', iResp)

                pre_key = response_key # Button status update
                preAnswer_time = current_time # Time stampe update

            pre_status = response_status  
        img = visual.ImageStim(win = my_win, image = img_rest, units = 'pix')
        img.draw()
        my_win.flip()
        core.wait(2)


# Thank u
img = visual.ImageStim(win = my_win, image = img_ty, 
                       units = 'pix')
img.draw()
my_win.flip()
core.wait(2)

# Close the window
my_win.close()