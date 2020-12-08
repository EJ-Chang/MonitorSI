# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 2020

Written by EJ_Chang
"""

import os
from os import listdir
from os.path import isfile, join

fileMapping = {
    'OSD' : {
        'Directory' : '/Users/YJC/Dropbox/ExpRecord_HSI/D_1',
        'MergeName' : 'OSD_D_Merge.txt'
        },
    'OSD_Rev' : {
        'Directory' : '/Users/YJC/Dropbox/ExpRecord_HSI/D_1_Rev',
        'MergeName' : 'OSD_D_Rev_Merge.txt'
        },
    'ACC' : {
        'Directory' : '/Users/YJC/Dropbox/ExpRecord_HSI/D_ACC',
        'MergeName' : 'ACC_D_Merge.txt'
        },
    'RT' : {
        'Directory' : '/Users/YJC/Dropbox/ExpRecord_HSI/D_RT',
        'MergeName' : 'RT_D_Merge.txt'
        }

}


# Subject profile

whichExp = input("Which experiment data do you want to merge? ").upper()
print('OK, experiment %s is processing...' % whichExp)

# Go to the choosen directory 
os.chdir(fileMapping[whichExp]['Directory'])
# Get file list
fileList = os.listdir(fileMapping[whichExp]['Directory'])

dataFiles = []
for files in fileList:
    if (files.endswith('.txt') and files.startswith('2020')):
        dataFiles.append(files)

# Initial value
dataMerge = []
ID = 0

# Read files from the list, adding ID to is
for data in dataFiles:
    f = open(data, 'r')
    ID += 1
    print(ID)
    dataSet = f.readlines()

    # Merge them
    for line in dataSet:
        if 'NoMeaning' in line:
            pass
        else:
            dataMerge.append([ID,line[:-1]])
            # Save lines
            with open(fileMapping[whichExp]['MergeName'], 'w') as filehandle: 
                for key in dataMerge:
                    for item in key:
                        filehandle.writelines('%s ' % item)
                    filehandle.writelines('\n')

