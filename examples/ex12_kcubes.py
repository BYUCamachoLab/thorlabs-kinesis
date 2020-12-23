

import os
os.environ['PATH'] = "C:\\Program Files\\ThorLabs\\Kinesis" + ";" + os.environ['PATH']

from threading import Thread
import thorlabs_kinesis as tk
import time
from ctypes import (
    c_short,
    c_char_p,
    c_void_p,
    byref,
    c_uint,
    c_int,
    c_double,
    create_string_buffer,
)
from ctypes.wintypes import (
    DWORD,
    WORD,
)
# class Static_Vars:
#     steps_per_mm = 34304

from thorlabs_kinesis import kcube_dcservo as kcdc

if kcdc.TLI_BuildDeviceList() == 0:
    print("Device list built (no errors).")

    size = kcdc.TLI_GetDeviceListSize()
    print(size, "device(s) found.")

    serialnos = create_string_buffer(100)
    kcdc.TLI_GetDeviceListByTypeExt(serialnos, 100, 27)
    serialnos = list(filter(None, serialnos.value.decode("utf-8").split(',')))
    print("Serial #'s:", serialnos)
    
    serialno = c_char_p(bytes("27504851", "utf-8"))

    device_info = kcdc.TLI_DeviceInfo()
    kcdc.TLI_GetDeviceInfo(serialno, byref(device_info))
    print("Device info:", device_info)

    accel_param = c_int()
    vel_param = c_int()
    current_motor_pos = 0

    move_pos=2000
    motor_command = c_int(move_pos)

    # Open Communication
    kcdc.CC_Open(serialno)
    kcdc.CC_StartPolling(serialno, c_int(200))
    kcdc.CC_ClearMessageQueue(serialno)
    kcdc.CC_LoadSettings(serialno)
    kcdc.CC_EnableChannel(serialno)
    kcdc.CC_RequestSettings(serialno)
    # time.sleep(3)
    # msg_type, msg_id, msg_data = WORD(), WORD(), DWORD()
    # kcdc.CC_WaitForMessage(serialno, byref(msg_type), byref(msg_id), byref(msg_data))
    # print("type, id: {}, {}".format(msg_type.value, msg_id.value))
    # while msg_type.value != 1 or msg_id.value != 0:
    #     kcdc.CC_WaitForMessage(serialno, byref(msg_type), byref(msg_id), byref(msg_data))
    #     print("type, id: {}, {}".format(msg_type.value, msg_id.value))

    # Test CC_GetDeviceUnitFromRealValue
    real_value = c_double(25.0)
    device_unit = c_int()
    kcdc.CC_GetDeviceUnitFromRealValue(serialno, real_value, byref(device_unit), c_int(0))
    print("Device unit of {}: {}".format(real_value.value, device_unit.value))

    # Test CC_CanHome
    homeable = bool(kcdc.CC_CanHome(serialno))
    print("Homeable:", homeable)

    #Get Motor Position
    kcdc.CC_GetJogVelParams(serialno, byref(accel_param), byref(vel_param))
    #print(accel_param.value)
    
    # #kcdc.CC_Home(serialno)

    # Start Move Test
    # kcdc.CC_ClearMessageQueue(serialno)
    # kcdc.CC_MoveToPosition(serialno, motor_command)
    # kcdc.CC_WaitForMessage(serialno, byref(message_type), byref(message_id), byref(message_data))

    # while (int(message_type.value) != 2) or (int(message_id.value) != 1):
    #     kcdc.CC_WaitForMessage(serialno, byref(message_type), byref(message_id), byref(message_data))
    #     kcdc.CC_RequestPosition(serialno)
    #     # I Get correct position feedback here
    #     print("TEST", kcdc.CC_GetPosition(serialno))

    # But I dont get correct position feedback here. I just get 0.
    kcdc.CC_RequestPosition(serialno)
    print("Current position:", kcdc.CC_GetPosition(serialno))

    # TEST CC_GetJogStepSize
    step = c_uint()
    step = kcdc.CC_GetJogStepSize(serialno)
    print("Step size (device units):", step)
    
    # Test CC_GetMotorTravelLimits
    minpos, maxpos = c_double(), c_double()
    kcdc.CC_GetMotorTravelLimits(serialno, byref(minpos), byref(maxpos))
    print("Min: {} Max: {}".format(minpos, maxpos))

    # Test CC_GetNumberPositions
    pos = kcdc.CC_GetNumberPositions(serialno)
    print("Number of positions:", pos)

    # Test CC_MoveJog
    kcdc.CC_MoveJog(serialno, kcdc.MOT_Reverse)
    kcdc.is_moving(serialno)

    # Get position again.
    kcdc.CC_RequestPosition(serialno)
    time.sleep(0.1)
    current_motor_pos = kcdc.CC_GetPosition(serialno)
    print("Current position:", current_motor_pos)

    # Close Communication
    kcdc.CC_StopPolling(serialno)
    kcdc.CC_Close(serialno)
