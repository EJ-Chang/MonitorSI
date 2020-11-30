# -*- coding: utf-8 -*-


import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 


# Preparing experiment stimulus
# img_start = 'OSD_ImgFolder/start.png'
# img_rest = 'OSD_ImgFolder/rest.png'
# img_ty = 'OSD_ImgFolder/thanks.png'
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


print(len(stimulus_seq))