
import os, random, time 
import pyfirmata # Communicate with Arduino
from psychopy import visual, event, core, monitors 
from ARDTrigger import * # Response trigger

# Prepare our Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()

# Name and assign input pins
sig_input_dc = board.get_pin('d:5:i') # dial - sw
sig_input_dx = board.get_pin('d:6:i') # dial - dt
sig_input_dy = board.get_pin('d:7:i') # dial - click
sig_input_bt = board.get_pin('d:10:i') # Omron


# Initial status of input pins
pre_stat = []
pre_resp_status = []
trigger = []
hw_required = 'Dial'


startTime = core.getTime()
currentTime = core.getTime()

while currentTime - startTime  < 10:
    currentTime = core.getTime()
    trigger_wait = 1
    resp_status = 1

    while trigger_wait == 1:
        # Read ports of required hardware ==== 
        if hw_required == 'Joystick':
            joy_x = sig_input_jx.read()
            joy_y = sig_input_jy.read()
            joy_c = sig_input_jc.read()
            # Get joystick function
            resp_key, trigger_wait =  getJoystick(joy_x, joy_y, joy_c)

        elif hw_required == 'Dial':
            dial_c = sig_input_dc.read()
            dial_x = sig_input_dx.read()
            dial_y = sig_input_dy.read()
            dial_b = sig_input_bt.read()
            # Get dial function
            resp_key, resp_status, trigger_wait, trigger = getDial(dial_c, dial_x, dial_y, dial_b,
                                                                    pre_resp_status, trigger, resp_status)
            pre_resp_status = resp_status

            # print(trigger)
