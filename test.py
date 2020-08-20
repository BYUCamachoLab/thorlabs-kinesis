# equipment: Thorlabs Benchtop Piezo BCP 303 (3 channel piezo controller)
#            connected to ThorLabs NanoMax 300 Stage (3 Channel)

# Simply turn off unused devices then execute this file in the Anaconda Prompt

# July 28, 2020
# Davin Fish
# email: davotrey@gmail.com

import os
os.environ['PATH'] = "C:\\Program Files\\ThorLabs\\Kinesis" + ";" + os.environ['PATH']
#print(os.environ['PATH']) 
from threading import Thread
import thorlabs_kinesis as tk
import time
import keyboard
from ctypes import (
    c_short,
    c_char_p,
    c_void_p,
    byref,
    c_int,
    create_string_buffer,
)
from ctypes.wintypes import (
    DWORD,
    WORD,
)

from thorlabs_kinesis import benchtop_piezo as bp

# clears the keyboard buffer
def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
# to prevent multiple prints/actions per key press
def keyDebounce():
    time.sleep(0.2) # sleep 200 ms 

# Home the stages at half-of-travel so they can be used to do slight adjustments
def homeStages():
    halfway = c_short(16383)    # half of travel 
    bp.PBC_SetPosition(serialno,bp.Channel1,halfway)    # set the position
    bp.PBC_SetPosition(serialno,bp.Channel2,halfway)
    bp.PBC_SetPosition(serialno,bp.Channel3,halfway)
    print("Stages Homing, waiting 3 sec to settle...")  # in the case of zeroing, there may be some settle-time
    time.sleep(3)
    print("done")

# increase the position of a provided channel by a certain joglength
def upShift(jogLength,channel):
    currentPos = int(bp.PBC_GetPosition(serialno,channel))
    bp.PBC_SetPosition(serialno,channel,c_short(currentPos + jogLength))

# decrease the position of a provided channel by a certain joglength
def downShift(jogLength,channel):
    currentPos = int(bp.PBC_GetPosition(serialno,channel))
    bp.PBC_SetPosition(serialno,channel,c_short(currentPos - jogLength))

# allows for more direct control of the x channel movement
def move():
    print("Press 'w' to shift 10 nm forward\nPress 's' to shift 80 nm backward\nPress 'e' to shift 5 nm forward\nPress 'd' to shift 5nm backward\nPress 'q' to exit function")
    Done = False
    keyDebounce() # key 'debouncer'
    medium = int(16)        # 10 nm
    small = int(8)          # 5 nm
    extraLarge = int(200)   # 125 nm

    # look for key presses, q reverts to main menu
    while not Done:
        try:
            if keyboard.is_pressed('q'):
                keyDebounce() # key 'debouncer'
                print("Moving Complete")
                flush_input()
                return
            elif keyboard.is_pressed('w'):
                keyDebounce() # key 'debouncer'
                upShift(medium,bp.Channel1)    # shift forward 10 nm
                print("shifted forward",round(medium/8*5),"nm")
                time.sleep(0.1)
            elif keyboard.is_pressed('s'):
                keyDebounce() # key 'debouncer'
                downShift(extraLarge,bp.Channel1) # shift backwards 125 nm
                print("shifted backward",round(extraLarge/8*5),"nm")
            elif keyboard.is_pressed('e'):
                keyDebounce() # key 'debouncer'
                upShift(small,bp.Channel1)    # shift forward 5 nm
                print("shifted forward",round(small/8*5),"nm")
            elif keyboard.is_pressed('d'):
                keyDebounce() # key 'debouncer'
                downShift(small,bp.Channel1) # shift backwards 5 nm
                print("shifted backward",round(small/8*5),"nm")
        except:
            continue

# for coupling a resonator to a stationary tapered fiber
# draws the resonator closer (x channel/axis) at a variable rate
# stopping the movement draws back and enters the move state
# for more fine control of the coupling, good for coupling at a gap
def couple():
    print("Press 'w' to increase jog step forward (accelerate)\nPress 's' to decrease jog step forward (decelerate)\nPress 'q' to exit function\n\nStarted Motion towards Fiber...")
    jogLength = int(16) # just under 10 nm of travel
    retreatLength = int(64) # 40 nm travel
    Done = False        # while loop bool
    printCounter = 0
    while not Done:
        try: 
            if keyboard.is_pressed('q'):    # press q to exit the while loop and stop motion
                keyDebounce() # key 'debouncer'
                print('Coupling Movement Stopped')
                flush_input()   # clear keybaord buffer
                downShift(retreatLength,bp.Channel1)    # as we stop the coupling command, retreat 40 nm (64)    
                move()  # call the move function                    
                return
            elif keyboard.is_pressed('w'):  # press w to increase the rate of motion
                keyDebounce() # key 'debouncer'
                jogLength += int(2)
                print("jogLength: ", jogLength)
            elif keyboard.is_pressed('s'):  # press s to decrease the rate of motion
                if jogLength > 4:
                    keyDebounce() # key 'debouncer'
                    jogLength -= int(2)
                    print("jogLength: ", jogLength)
        except: 
            continue
        upShift(jogLength,bp.Channel1)  # translate forward for the adjustable jogLength
        if printCounter == 25:
            print("Travel in um: ",round(int(bp.PBC_GetPosition(serialno,bp.Channel1))/8*5/1000,2))
            printCounter = 0
        printCounter += 1 
        time.sleep(0.2)

# allows for rough adjustment of the y and z channels
def adjust(channel):
    print("Press 'w' to shift 0.5 um up or right\nPress 's' to shift 0.5 um down or left\nPress 'q' to exit function")
    jogLength = 800 # about half a micron out of 20 um of 
    currentPos = int(0) 
    Done = False 
    while not Done:
        try: 
            if keyboard.is_pressed('q'):    # press q to exit the while loop and stop motion
                keyDebounce() # key 'debouncer'
                print('Adjustment Complete')
                flush_input()   # clear the keyboard buffer
                return
            elif keyboard.is_pressed('w'):  # press w to shift up or right
                keyDebounce() # key 'debouncer'
                currentPos = int(bp.PBC_GetPosition(serialno,channel))
                if currentPos < maxTravel - jogLength:
                    upShift(jogLength,channel)
                    print("shifted channel:",channel," forward",round(jogLength/8*5/1000,1),"um")
                else:
                    print("Max travel reached")
            elif keyboard.is_pressed('s'):  # press s to shift down or left
                keyDebounce() # key 'debouncer'
                downShift(jogLength,channel)
                print("shifted channel:",channel," backward",round(jogLength/8*5/1000,1),"um")
        except: 
            continue



maxTravel = 32767 # travel is from 0 to 32767 for 20 um
if bp.TLI_BuildDeviceList() == 0:   # if there are devices properly built
    print("Device list built (no errors).")
    size = bp.TLI_GetDeviceListSize()   # finds the amount of devices seen
    print(size, "device(s) found.")
    if size > 0:    # if at least one thor labs device is found

        # Open Communication
        serialno = c_char_p(bytes("71854093", "utf-8")) # the 8 digit serial number on the back of the piezo controller
        bp.PBC_Open(serialno)       # open the device for communication
        bp.PBC_StartPolling(serialno,bp.Channel1,c_int(200))    # start polling each channel every 200 ms
        bp.PBC_StartPolling(serialno,bp.Channel2,c_int(200))
        bp.PBC_StartPolling(serialno,bp.Channel3,c_int(200))
        bp.PBC_ClearMessageQueue(serialno)  # clear prior messages
        time.sleep(1)   # pause 1 sec

        # Initialize/Identify Channels

        # x axis
        bp.PBC_EnableChannel(serialno, bp.Channel1) # enables control of specified channel
        bp.PBC_SetZero(serialno, bp.Channel1)   # set the voltage to 0, then define that position as 0
        #bp.PBC_Identify(serialno, bp.Channel1)  # cause the LED readout to blink to identify it
        print("zeroing channel 1")

        # y axis
        bp.PBC_EnableChannel(serialno, bp.Channel2)
        bp.PBC_SetZero(serialno, bp.Channel2)   # set the voltage to 0, then define that position as 0
        # bp.PBC_Identify(serialno, bp.Channel2)
        print("zeroing channel 2")

        # z axis
        bp.PBC_EnableChannel(serialno, bp.Channel3)
        bp.PBC_SetZero(serialno, bp.Channel3)   # set the voltage to 0, then define that position as 0
        # bp.PBC_Identify(serialno, bp.Channel3)
        print("zeroing channel 3")
        time.sleep(40)

        #Identify Control Mode TODO: remove this code after testing 
        print("control type for bp.Channel1: ", bp.PBC_GetPositionControlMode(serialno,bp.Channel1))
        print("control type for bp.Channel2: ", bp.PBC_GetPositionControlMode(serialno,bp.Channel2))
        print("control type for bp.Channel3: ", bp.PBC_GetPositionControlMode(serialno,bp.Channel3))

        homeStages()

        Done = False
        while not Done:
            command = input("Enter a key to perform an action (? for help): ")
            if command is 'h':
                homeStages()
            elif command is 'c':
                couple()
            elif command is 'm':
                move()
            elif command is 'z':
                adjust(bp.Channel3)
            elif command is 'y':
                adjust(bp.Channel2)
            elif command is '?':
                print('\nh -------- home the three axis\nc -------- couple (q to quit, w to speed up, s to slow down)\nm -------- move x axis at different step sizes\nz -------- adjust z axis (q to quit, w to move up, s to move down)\ny -------- adjust y axis (q to quit, w to move up, s to move down)\nq -------- quit')
            elif command is 'q':
                Done = True

        
        bp.PBC_StopPolling(serialno,bp.Channel1)
        bp.PBC_StopPolling(serialno,bp.Channel2)
        bp.PBC_StopPolling(serialno,bp.Channel3)
        if bp.PBC_Disconnect(serialno) == 0:
            print("device disconnected")
        bp.PBC_Close(serialno)
        flush_input()