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

if bp.TLI_BuildDeviceList() == 0:
    print("Device list built (no errors).")
    size = bp.TLI_GetDeviceListSize()   # finds the amount of devices seen
    print(size, "device(s) found.")
    serialno = c_char_p(bytes("71874833", "utf-8")) # the 8 digit serial number on the back of the piezo controller
    bp.PBC_Open(serialno)       # open the device for communication
    bp.PBC_StartPolling(serialno,bp.Channel1,c_int(200))    # start polling each channel every 200 ms
    bp.PBC_ClearMessageQueue(serialno)  # clear prior messages
    time.sleep(1)   # pause 1 sec
    bp.PBC_EnableChannel(serialno, bp.Channel1) # enables control of specified channel
    #bp.PBC_SetZero(serialno, bp.Channel1)
    for i in (0,1,2,3,4,5,6,7,8,9,10):
        pos = bp.PBC_GetPosition(serialno,bp.Channel1);
        print(pos)
        time.sleep(1)