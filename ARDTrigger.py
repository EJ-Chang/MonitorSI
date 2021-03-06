# -*- coding: utf-8 -*-
"""
Created on Wed Nov 4 2020

Written by EJ_Chang
"""

from psychopy import visual, event, core, monitors


# def getJoystick(joy_x, joy_y, joy_c):
#     print(joy_x, joy_y, joy_c)

#     if [joy_x, joy_y, joy_c] == [True, True, True]: # WRONGG!!!!!! first 2 digits are numbers not boolean
#         trigger_wait = 1
#         resp_key = 'None'
#     else:
#         trigger_wait = 0 
#         resp_key = 'None'
#         # Get trigger meaning
#         if joy_c == False:
#             resp_key = 'Click'

#         elif joy_c == True:
#             D1 = joy_y - joy_x
#             D2 = joy_y + joy_x - 1
#             O1 = (joy_x-0.5) ** 2 + (joy_y-0.5) ** 2 - 0.04 # r = 0.2
#             if O1 >= 0:
#                 if D1 > 0 and D2 > 0:
#                     resp_key = 'Up'
#                 elif D1 < 0 and D2 > 0:
#                     resp_key = 'Left'
#                 elif D1 < 0 and D2 < 0:
#                     resp_key = 'Down'
#                 elif D1 > 0 and D2 < 0:
#                     resp_key = 'Right'
#             else:
#                 pass

#     return resp_key, trigger_wait



def getJoystick(joy_x, joy_y, joy_c):
    # print(joy_x, joy_y, joy_c)
    trigger_wait = 1
    resp_key = 'None'

    # Get trigger meaning
    if joy_c == False:
        resp_key = 'Click'
        trigger_wait = 0

    elif joy_c == True:
        D1 = joy_y - joy_x
        D2 = joy_y + joy_x - 1
        O1 = (joy_x-0.5) ** 2 + (joy_y-0.5) ** 2 - 0.04 # r = 0.2
        if O1 >= 0:
            trigger_wait = 0
            if D1 > 0 and D2 > 0:
                resp_key = 'Up'
            elif D1 < 0 and D2 > 0:
                resp_key = 'Left'
            elif D1 < 0 and D2 < 0:
                resp_key = 'Down'
            elif D1 > 0 and D2 < 0:
                resp_key = 'Right'
        else:
            trigger_wait = 1
            resp_key = 'None'
            

    return resp_key, trigger_wait



def getDial(click, x, y, button, pre_resp_status, trigger, resp_status):

    trigger_wait = 1
    resp_key = 'None'

    # Click status info
    if click == False:
        resp_key = 'Click'
        trigger_wait = 0
    elif button == True:
        resp_key = 'Button'
        trigger_wait = 0
    else:
        pass

    # Rotation position info
    rotation_pos = [x, y] # rotation x,y
    # Clockwise / counter-clockwise
    if rotation_pos == [True, True]:
        resp_status = 1
        
        if len(trigger) >= 2:
            if trigger[-1] - trigger[0] < 0:
                resp_key = 'CW'
                trigger_wait = 0
                # log.append('Clockwise >>>')
                # print(resp_key)
            elif trigger[-1] - trigger[0] > 0:
                resp_key = 'C_CW'
                trigger_wait = 0
                # log.append('<<< Counter-Clockwise')
                # print(resp_key)
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


    return resp_key, resp_status, trigger_wait, trigger


def response_check(resp_key, iRow, iCol, reqRow, reqCol):
    if resp_key == 'Click' or resp_key == 'Right':
        if [iRow, iCol] == [reqRow, reqCol]:
            final_answer = 1
        else:
            final_answer = 0
    else:
        final_answer = 0

    return final_answer


def determine_UI(hw_required, resp_key, iRow, iCol):

    if hw_required == 'Joystick':
        if resp_key == 'Up':
            iRow -= 1 
            if iRow <= 0:
                iRow = 0
        elif resp_key == 'Down':
            iRow += 1 
            if iRow >= 4:
                iRow = 4
        elif resp_key == 'Left':
            iCol -= 1 
            if iCol <= 0:
                iCol = 0
        elif resp_key == 'Right':
            iCol += 1 
            if iCol >= 3:
                iCol = 3
        elif resp_key == 'Click':
            iCol += 1 
            if iCol >= 3:
                iCol =3
        else:
            pass

    elif hw_required == 'Dial':
        if resp_key == 'C_CW':
            iRow -= 1 
            if iRow <= 0:
                iRow = 0
        elif resp_key == 'CW':
            iRow += 1 
            if iRow >= 4:
                iRow = 4
        elif resp_key == 'Button':
            iCol -= 1 
            if iCol <= 0:
                iCol = 0
        elif resp_key == 'Click':
            iCol += 1 
            if iCol >= 3:
                iCol =3
        else:
            pass
    else:
        pass

    return iRow, iCol


# ========


def getDialRev(click, x, y, button, pre_resp_status, trigger, resp_status):

    trigger_wait = 1
    resp_key = 'None'

    # Rotation position info
    rotation_pos = [x, y] # rotation x,y
    # Clockwise / counter-clockwise
    if rotation_pos == [True, True]:
        resp_status = 1
        
        if len(trigger) >= 2:
            if trigger[-1] - trigger[0] < 0:
                resp_key = 'C_CW'
                trigger_wait = 0
                # log.append('Clockwise >>>')
                # print(resp_key)
            elif trigger[-1] - trigger[0] > 0:
                resp_key = 'CW'
                trigger_wait = 0
                # log.append('<<< Counter-Clockwise')
                # print(resp_key)
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

    # Click status info
    if click == False:
        resp_key = 'Click'
        trigger_wait = 0
    elif button == True:
        resp_key = 'Button'
        trigger_wait = 0
    else:
        pass

    return resp_key, resp_status, trigger_wait, trigger

def getJoystickRev(joy_x, joy_y, joy_c):

    if [joy_x, joy_y, joy_c] == [True, True, True]:
        trigger_wait = 1
        resp_key = 'None'
    else:
        trigger_wait = 0
        resp_key = 'None'
        # Get trigger meaning
        if joy_c == False:
            resp_key = 'Click'

        elif joy_c == True:
            D1 = joy_y - joy_x
            D2 = joy_y + joy_x - 1
            O1 = (joy_x-0.5) ** 2 + (joy_y-0.5) ** 2 - 0.04 # r = 0.2
            if O1 >= 0:
                if D1 > 0 and D2 > 0:
                    resp_key = 'Up'
                elif D1 < 0 and D2 > 0:
                    resp_key = 'Right'
                elif D1 < 0 and D2 < 0:
                    resp_key = 'Down'
                elif D1 > 0 and D2 < 0:
                    resp_key = 'Left'
            else:
                pass

    return resp_key, trigger_wait


# Function : interpret ----
def interpret_key(hw_required, resp_key):
    key_meaning = 'None'
    # Setting key map
    if hw_required == 'Dial':
        if resp_key == 'CW':
            key_meaning = 'Down'
        elif resp_key == 'C_CW':
            key_meaning = 'Up'
        elif resp_key == 'Click':
            key_meaning = 'Right'
        elif resp_key == 'Button':
            key_meaning = 'Left'
    elif hw_required == 'Joystick':
        key_meaning = resp_key

    else:
        key_meaning = 'None'

    return key_meaning




# Function : match or not ----
def reponse_check(key_meaning, key_required):

    if key_meaning == key_required:
        final_answer = 1

    else:
        final_answer = 0

    return final_answer
