import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem14601')

while True:
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)