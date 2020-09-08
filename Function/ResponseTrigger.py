# -*- coding: utf-8 -*-
"""
Created on Tue Apr 7 2020

Written by EJ_Chang
"""
from psychopy import visual, event, core, monitors

'''
For RT exp
'''

# Function : get inputs from all devices
def getAnything(mouse, joy):
    '''
    Get every input device used in this project 
    '''
    clicks = mouse.getPressed()
    wheel = list(mouse.getWheelRel())
    # dPad = joy.getAllHats()
    dPad = list(joy.getAllHats()[0])
    but_x = int(joy.getButton(0))
    buttons = [but_x] # Can be modified to collect more buttons

    if clicks != [0, 0, 0]:
        response_status = 1
        response_hw = 'Mouse'
        response_key = clicks
    elif wheel != [0, 0]:
        response_status = 1
        response_hw = 'Wheel'
        response_key = wheel
    # elif dPad != [(0, 0)] and len(dPad) > 0:
    elif dPad != [0, 0] and len(dPad) > 0:
        response_status = 1
        response_hw = 'dPad'
        response_key = dPad
    elif buttons != [0]:
        response_status = 1
        response_hw = 'Buttons'
        response_key = buttons
    else:
        response_status = 0
        response_hw = 'NoMeaning'
        response_key = []

    return response_hw, response_key, response_status

# Function : interpret ----
def interpret_key(response_hw, response_key):
    '''
    Translate input signals to meaningful words/tags for later usage
    '''

    # Setting key map
    if response_hw == 'Mouse':

        if response_key[0] == 1:
            key_meaning = 'NoMeaning'
        elif response_key[1] == 1:
            key_meaning = 'OK'
        elif response_key[2] == 1:
            key_meaning = 'NoMeaning'

    elif response_hw == 'Wheel':
        if response_key[1] < 0:
            key_meaning = 'Up'
        elif response_key[1] > 0:
            key_meaning = 'Down'
        elif response_key[0] > 0:
            key_meaning = 'Left'
        elif response_key[0] < 0:
            key_meaning = 'Right'

    elif response_hw == 'dPad':
        if response_key == [0, 1]:
            key_meaning = 'Up'
        elif response_key == [0, -1]:
            key_meaning = 'Down'
        elif response_key == [-1, 0]:
            key_meaning = 'Left'
        elif response_key == [1, 0]:
            key_meaning = 'Right'
        elif response_key[0] != 0 and response_key[1] != 0:
            key_meaning = 'OK'
        else:
            key_meaning = 'NoMeaning'

    elif response_hw == 'Buttons':
        if response_key[0] == 1:
            key_meaning = 'Abort'

    return key_meaning


# Function : match or not ----
def reponse_checker(response_hw, key_meaning, stimlus_dictionary):
    '''
    Check if the response(input) was right or wrong
    '''

    key_judgement = [0, 0]
    if response_hw == stimlus_dictionary['hardware']:
        key_judgement[0] = 1
    else:
        key_judgement[0] = 0

    if key_meaning == stimlus_dictionary['meaning']:
        key_judgement[1] = 1
    else:
        key_judgement[1] = 0

    final_answer = key_judgement[0] * key_judgement[1]

    return key_judgement, final_answer


# Function : determinant ----
def determine_behavior(key_meaning, item, nTrials, expStatus):
    '''
    Determine how should the program react to the input
    '''

    if key_meaning == 'Abort':
        expStatus = 0

    elif key_meaning == 'Up' or 'Down' or 'Left' or 'Right':
        item += 1
        if item > nTrials - 1:
            item = nTrials - 1
            expStatus = 0

    return item, expStatus

'''
For ACC exp
'''

# Function : interpret ----
def interpret_key_ACC(response_hw, response_key):

    # Setting key map
    if response_hw == 'Mouse':
        key_meaning = 'NoMeaning'
        # if response_key[1] == 1:
        #     key_meaning = 'OK'
        # else:
        #     key_meaning = 'NoMeaning'

    elif response_hw == 'Wheel':
        if response_key[1] < 0:
            key_meaning = 'Up'
        elif response_key[1] > 0:
            key_meaning = 'Down'
        elif response_key[0] > 0:
            key_meaning = 'Left'
        elif response_key[0] < 0:
            key_meaning = 'Right'

    elif response_hw == 'dPad':
        if response_key == [0, 1]:
            key_meaning = 'Up'
        elif response_key == [0, -1]:
            key_meaning = 'Down'
        elif response_key == [-1, 0]:
            key_meaning = 'Left'
        elif response_key == [1, 0]:
            key_meaning = 'Right'
        else:
            key_meaning = 'NoMeaning'

    elif response_hw == 'Buttons':
        if response_key[0] == 1:
            key_meaning = 'Abort'

    return key_meaning


# Function : match or not ----
def reponse_checker_ACC(iResp, key_meaning, tag_que):

    final_answer = 0
    if key_meaning == tag_que[iResp]:
        final_answer = 1
    else:
        final_answer = 0

    return final_answer


# Function : match or not ----
def reponse_checker_ACC(response_hw, key_meaning, hw_required, key_required):

    key_judgement = [0, 0]
    if response_hw == hw_required:
        key_judgement[0] = 1
    else:
        key_judgement[0] = 0

    if key_meaning == key_required:
        key_judgement[1] = 1
    else:
        key_judgement[1] = 0

    final_answer = key_judgement[0] * key_judgement[1]

    return final_answer



'''
For OSD simulation 
'''


# Function : determinant ----
def determine_behavior_OSD(key_meaning, iRow, iCol, 
    nRow = 4, nCol = 3, trialStatus = 1):

    if key_meaning == 'Abort':
        trialStatus = 0
        core.quit()

    elif key_meaning == 'Up':
        iRow -= 1
        if iRow <= 0:
            iRow = 0

    elif key_meaning == 'Down':
        iRow += 1
        if iRow >= nRow:
            iRow = nRow

    elif key_meaning == 'Left':
        if iCol <= 0:
            iCol = 0
        else:
            iCol -= 1
            iRow = 0

    elif key_meaning == 'NoMeaning':
        iCol += 0


    elif key_meaning == 'Right' or 'OK':
        if iCol >= nCol:
            iCol = nCol
        else:
            iCol += 1
            iRow = 0


    return iRow, iCol, trialStatus


# Function : match or not ----
def reponse_checker_OSD(req_hw, response_hw, iRow, iCol, reqRow, reqCol,
                        nRow = 4 , nCol = 3):
    
    # Initial value
    key_judgement = [0,0]

    # For key judgement 1
    if req_hw == 'Wheel': # if wheel
        if response_hw == req_hw or response_hw == 'Mouse':  # add buttons as an exception
            key_judgement[0] = 1
        else:
            key_judgement[0] = 0
    else: # if not wheel 
        if response_hw == req_hw:
            key_judgement[0] = 1
        else:
            key_judgement[0] = 0

    # For key judgement 2
    if (iRow == reqRow and iCol == reqCol):
        key_judgement[1] = 1
    else:
        key_judgement[1] = 0

    final_answer = key_judgement[0] * key_judgement[1]

    return key_judgement, final_answer


'''
For Button simulation
'''

# Function : determinant ----
def determine_behavior_BTS(key_meaning, iRow, iCol, 
    nRow = 4, nCol = 3, trialStatus = 1):

    if key_meaning == 'Abort':
        # trialStatus = 0
        core.quit()

    elif key_meaning == 'Up':
        iRow -= 1
        if iRow <= 0:
            iRow = 0

    elif key_meaning == 'Down':
        iRow += 1
        if iRow >= nRow:
            iRow = nRow

    elif key_meaning == 'Left':
        if iCol <= 0:
            iCol = 0
        else:
            iCol -= 1
            iRow = 0
            
    elif key_meaning == 'NoMeaning':
        iCol += 0

    elif key_meaning == 'Right' or 'OK':
        if iCol >= nCol:
            iCol = nCol
        else:
            iCol += 1
            iRow = 0

    return iRow, iCol, trialStatus


# Function : match or not ----
def reponse_checker_BTS(BUTTON_STATUS, req_hw, response_hw, key_meaning, iRow, iCol,
                        reqRow, reqCol, nRow = 4 , nCol = 3):

    key_judgement = [0,0]
    # For key judgement 1
    if req_hw == 'Wheel': # if wheel
        if response_hw == req_hw or response_hw == 'Mouse':  # add buttons as an exception
            key_judgement[0] = 1
        else:
            key_judgement[0] = 0
    else: # if not wheel 
        if response_hw == req_hw:
            key_judgement[0] = 1
        else:
            key_judgement[0] = 0

    # For key judgement 2
    if (iRow == reqRow and iCol == reqCol):
        key_judgement[1] = 1
    else:
        key_judgement[1] = 0

    final_answer = key_judgement[0] * key_judgement[1]

    if final_answer == 1:
        if key_meaning == 'OK' or key_meaning == 'Right':
            if BUTTON_STATUS == 'on':
                BUTTON_STATUS = 'off'
            elif BUTTON_STATUS == 'off':
                BUTTON_STATUS = 'on'

    return final_answer, BUTTON_STATUS

