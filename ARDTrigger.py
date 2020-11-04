# -*- coding: utf-8 -*-
"""
Created on Wed Nov 4 2020

Written by EJ_Chang
"""

from psychopy import visual, event, core, monitors



def getPorts(joystick, dial):

    # Now I have joystick and dial
    joystick = [tg_jx, tg_jy, tg_jc]
    dial = [tg_sw, tg_dt, tg_cl, tg_om]

    if joystick != [False, False, False]:
        response_status = 1
        response_hw = 'Joystick'
    elif dial != [False, False, False, False]:
        response_status = 1
        response_hw = 'Dial'







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

# ====


def nothing():

        # Click status info
        click_stat = tg_cl

        if click_stat == False and pre_click == True:
            clickTime = core.getTime()
            if clickTime - pre_clickTime > 0.1:
                iCol += 1
                print('Click')
                if iCol > 3:
                    iCol = 0

            trigger_wait = 0
            pre_clickTime = clickTime
        else:
            pass

        pre_click = tg_cl
 

        # Button(back key) status info
        button_stat = tg_om

        if button_stat == False and pre_button == True:
            buttonTime = core.getTime()
            if buttonTime - pre_buttonTime > 0.1:
                iCol -= 1
                print('Back')
                if iCol <= 0:
                    iCol = 0
            trigger_wait = 0
            pre_buttonTime = buttonTime
        else:
            pass

        pre_button = tg_om


        # Rotation position info
        rotation_pos = [tg_sw, tg_dt] # rotation x,y

        # Clockwise / counter-clockwise
        if rotation_pos == [True, True]:
            resp_status = 1
            
            if len(trigger) >= 2:
                if trigger[-1] - trigger[0] < 0:
                    print('Clockwise >>>')
                    iRow += 1
                    if iRow >= 4:
                        iRow = 4
                    # log.append('Clockwise >>>')
                    trigger_wait = 0
                elif trigger[-1] - trigger[0] > 0:
                    print('<<< Counter-Clockwise')
                    iRow -= 1
                    if iRow <= 0:
                        iRow = 0
                    trigger_wait = 0
                    # log.append('<<< Counter-Clockwise')
                else:
                    pass
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


        pre_stat = [tg_sw, tg_dt]
        pre_resp_status = resp_status
