# -*- coding: utf-8 -*-
"""
Created on Mon May 11 2020

Written by EJ_Chang
"""

from datetime import date
from psychopy import visual, event, core, monitors
import pyfirmata # Communicate with Arduino
import numpy as np
from StiGenerator import *
from Solarized import * # Solarized color palette
from GUI_Material import * # Prototype OSD GUI
from ARDTrigger import * # Response trigger


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
#                        color=SOLARIZED['base03'], colorSpace='rgb255', 
#                        monitor = mon, units = 'pix', 
#                        screen = 1)

# my_win = visual.Window(size=(2560, 1440), pos=(0,0), monitor = mon, units = 'pix', 
#                        screen = 0, fullscr = 1)
# my_win = visual.Window(size=(2560, 1440), pos=(0,0), 
#                        color=base03, colorSpace='rgb255', 
#                        monitor = mon, units = 'pix', 
#                        screen = 0, fullscr = 1)

my_win = visual.Window(size=(2560, 1440), pos=(0,0), 
                       color=SOLARIZED['base03'], colorSpace='rgb255', 
                       monitor = mon, units = 'pix', 
                       screen = 0, fullscr = 1)


# Preparing Arduino & Mouse ----

# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_jx = board.get_pin('a:3:i') # joystick - sx
sig_input_jy = board.get_pin('a:5:i') # joystick - sy
sig_input_jc = board.get_pin('d:8:i') # joystick - clk

# - Mouse setting
mouse = event.Mouse(visible = True, win = my_win)
mouse.clickReset() # Reset to its initials

# Preparing pics ----
img_start = 'Img/Practice_Start.png'
img_ty = 'Img/Practice_End.png'

img_ins1 = 'Img/Practice_Ins1.png'
img_ins2 = 'Img/Practice_Ins2.png'

# Setting Constants ----
ORIGIN_POINT = (0,0)
ORIGIN = visual.Circle(my_win, units =  'pix',
                       radius = 5, pos = ORIGIN_POINT,
                       fillColor = SOLARIZED['base01'], fillColorSpace = 'rgb255',
                       lineColor = SOLARIZED['base01'], lineColorSpace = 'rgb255', 
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
             'Left': LINE_LEFT, 'Right': LINE_RIGHT, 'None': LINE_NONE}
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
hw_required = 'Joystick'
currentTime = core.getTime()
# ===========================

# Start experiment ----
# Instruction

while 1:
    img = visual.ImageStim(my_win, image = img_ins1)
    img.draw()
    my_win.flip()
    clicks = mouse.getPressed()
    if clicks != [0, 0, 0]:
        break
core.wait(1)
while 1:
    img = visual.ImageStim(my_win, image = img_ins2)
    img.draw()
    my_win.flip()
    clicks = mouse.getPressed()
    if clicks != [0, 0, 0]:
        break

for nTrial in range(1): # trial number

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
                     'None': ROTATE_NONE}


    # =========================
    #  Trial start !
    # =========================
    loopStatus = 1
    iResp = 0
    resp_path = [ORIGIN_POINT, ORIGIN_POINT]
    key_meaning = 'None'
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
                           lineColor = SOLARIZED['base01'], lineColorSpace = 'rgb255', 
                           vertices = (sti_path[iLine+1], sti_path[iLine+2]),
                           closeShape = False, pos = (0, 0))
            stimuli_path.draw()

        # End point
        end = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3, 
              lineColor = SOLARIZED['base01'], lineColorSpace = 'rgb255', 
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
                            lineColor = SOLARIZED['green'], lineColorSpace = 'rgb255', 
                            vertices = (sti_path[iResp], sti_path[iResp+1]),
                            closeShape = False, pos = (0, 0))
            response_path.draw()


        # Indicator
        indicator_pos = resp_path[iResp+1]
        indicator_point = visual.Circle(my_win, units =  'pix',
                          radius = 4, pos = (indicator_pos),
                          fillColor = SOLARIZED['yellow'], fillColorSpace = 'rgb255',
                          lineColor = SOLARIZED['yellow'], lineColorSpace = 'rgb255', 
                          interpolate = True)
        indicator_point.draw()


        indicator_spine = indicator_pos + four_dict[key_meaning]

        indicator_line = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3,
                         lineColor = SOLARIZED['magenta'], lineColorSpace = 'rgb255',
                         vertices = (indicator_pos, indicator_spine),
                         closeShape = False, pos = (0,0))
        indicator_line.draw()

        indicator_arrow = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3,
                          lineColor = SOLARIZED['magenta'], lineColorSpace = 'rgb255',
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
        trigger_wait = 1


        '''
        Response routine
        '''

        # Get response 
        # response_hw, response_key, response_status = getAnything(mouse, joy)
        while trigger_wait == 1:
            # Read ports of required hardware ==== 
            joy_x = sig_input_jx.read()
            joy_y = sig_input_jy.read()
            joy_c = sig_input_jc.read()
            # Get joystick function
            resp_key, trigger_wait =  getJoystick(joy_x, joy_y, joy_c)
            key_meaning = interpret_key(hw_required, resp_key)


            if resp_key != pre_key:
              currentTime = core.getTime()
              # Check response =====
              final_answer = reponse_check(key_meaning, tag_que[iResp])

              # Collect response (data)
              if key_meaning != 'None':
                response.append([nTrial, iResp, resp_key, key_meaning,
                    tag_que[iResp], final_answer,
                    currentTime - preAnswer_time, currentTime
                    ]) # correct/not, RT, real time

              if final_answer == 1:
                  # key_meaning = 'None' # Reset key meaning
                  resp_path.append(sti_path[iResp+2])
                  iResp += 1
                  if iResp >= N_LINE:
                      iResp = N_LINE

                      for iResp in range(len(resp_path)-1):
                          response_path = visual.ShapeStim(my_win, units = 'pix', lineWidth = 3, 
                                          lineColor = SOLARIZED['green'], lineColorSpace = 'rgb255', 
                                          vertices = (sti_path[iResp], sti_path[iResp+1]),
                                          closeShape = False, pos = (0, 0))
                          response_path.draw()
                      ORIGIN.draw()
                      end.draw()
                      my_win.flip()
                      core.wait(0.5)
                      loopStatus = 0
                      # rest.draw()
                      core.wait(1)


            pre_key = resp_key # Button status update
            preAnswer_time = currentTime # Time stampe update


    core.wait(1)



# Close the window
my_win.close()
