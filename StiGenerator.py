# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 2020

Written by EJ_Chang
"""
import os, random


PseudoRandomPath = [
    ['1', '1', '1', '3', '1', '3', '1', '2', '1', '1'],
    ['0', '2', '0', '2', '2', '0', '2', '0', '2', '0'],
    ['0', '0', '0', '0', '3', '0', '0', '0', '2', '2'],
    ['1', '2', '1', '1', '1', '2', '1', '3', '3', '3'],
    ['2', '0', '0', '2', '1', '1', '2', '1', '1', '2'],
    ['0', '0', '0', '2', '2', '2', '2', '2', '0', '2'],
    ['1', '2', '2', '2', '1', '1', '1', '2', '1', '1'],
    ['2', '1', '2', '2', '2', '0', '0', '2', '0', '0'],
    ['1', '3', '1', '3', '3', '1', '3', '1', '2', '2'],
    ['1', '2', '1', '3', '3', '3', '3', '3', '3', '1'],
    ['0', '2', '2', '0', '3', '3', '0', '3', '0', '3'],
    ['2', '1', '2', '1', '2', '2', '1', '2', '2', '1'],
    ['1', '3', '1', '1', '1', '2', '1', '1', '1', '1'],
    ['2', '2', '1', '2', '2', '2', '0', '2', '0', '2'],
    ['1', '3', '1', '3', '1', '2', '1', '1', '1', '3'],
    ['0', '2', '0', '0', '2', '0', '0', '3', '0', '0'],
    ['3', '0', '0', '3', '0', '3', '3', '0', '3', '0'],
    ['2', '1', '1', '2', '1', '1', '1', '2', '2', '1'],
    ['3', '3', '1', '3', '1', '3', '0', '0', '3', '1'],
    ['1', '3', '1', '3', '3', '1', '3', '1', '1', '1'],
    ['3', '3', '1', '3', '1', '3', '3', '0', '3', '0'],
    ['1', '3', '3', '1', '2', '1', '3', '1', '2', '2'],
    ['0', '2', '2', '0', '0', '0', '2', '2', '2', '2'],
    ['0', '0', '2', '0', '3', '0', '0', '3', '3', '3'],
    ['0', '2', '2', '0', '0', '3', '3', '0', '0', '0'],
    ['0', '0', '0', '0', '2', '0', '2', '0', '0', '2'],
    ['1', '2', '1', '1', '1', '2', '1', '3', '3', '1'],
    ['2', '0', '0', '0', '2', '2', '2', '1', '2', '2'],
    ['2', '0', '0', '0', '0', '2', '2', '0', '0', '2'],
    ['1', '2', '1', '3', '1', '2', '2', '2', '2', '2']
]




# Function A: Generate line directions

def pathGenerate(dir_DictList):

    # Main directions
    # main_que = []
    # ortho_que = []
    sub_que = []
    for i in range(1): # Determine how many paths(nTrials) shall be generated.
        seed = random.randrange(4) # Random 0~3
        main = dir_DictList[seed]['main_dir'] # Random selected direction
        orthogonal = dir_DictList[seed]['ortho_dir'] # Orthogonal directions

        # Derivation directions (up to 3 choices)
        pre_que = main[:] # Copy main.
        sub_que.append(pre_que)
        que_pool = orthogonal[:] # Copy orthogonal. Avoid changning orthogonal
        que_pool += [main]

        for k in range(9):

            sequal = random.choice(que_pool)
            sub_que.append(sequal)

            if sequal in orthogonal:
                que_pool = [sequal, main]
            else:
                que_pool = orthogonal[:] # Copy orthogonal. Avoid changning orthogonal
                que_pool += [main]

            pre_que = sequal[:]

    return sub_que