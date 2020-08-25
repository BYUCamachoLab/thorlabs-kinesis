# -*- coding: utf-8 -*-
#
# Copyright © Thorlabs-Kinesis Project Contributors
# Licensed under the terms of the GNU GPLv3+ License
# (see thorlabs_kinesis/__init__.py for details)

"""
KCube DC Servo Motor
--------------------

Bindings for Thorlabs KCube DC Servo DLL.
Implemented with Kinesis Version 1.14.23.16838
"""

import enum
import time

import thorlabs_kinesis as tk

from ctypes import (
    Structure,
    cdll,
    c_bool,
    c_short,
    c_int,
    c_uint,
    c_int16,
    c_int32,
    c_char,
    c_byte,
    c_long,
    c_float,
    c_double,
    POINTER,
    CFUNCTYPE,
)

from thorlabs_kinesis._utils import (
    c_word,
    c_dword,
    bind
)

lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.DCServo.dll")


# enum MOT_MotorTypes
MOT_NotMotor = c_int(0)
MOT_DCMotor = c_int(1)
MOT_StepperMotor = c_int(2)
MOT_BrushlessMotor = c_int(3)
MOT_CustomMotor = c_int(100)
MOT_MotorTypes = c_int

# enum MOT_TravelDirection
class MOT_TravelDirection(enum.Enum):
    MOT_TravelDirectionDisabled = c_short(0)
    MOT_Forwards = c_short(1)
    MOT_Reverse = c_short(2)


class TLI_DeviceInfo(Structure):
    _fields_ = [("typeID", c_dword),
                ("description", (65 * c_char)),
                ("serialNo", (9 * c_char)),
                ("PID", c_dword),
                ("isKnownType", c_bool),
                ("motorType", MOT_MotorTypes),
                ("isPiezoDevice", c_bool),
                ("isLaser", c_bool),
                ("isCustomType", c_bool),
                ("isRack", c_bool),
                ("maxChannels", c_short)]


class TLI_HardwareInformation(Structure):
    _fields_ = [("serialNumber", c_dword),
                ("modelNumber", (8 * c_char)),
                ("type", c_word),
                ("firmwareVersion", c_dword),
                ("notes", (48 * c_char)),
                ("deviceDependantData", (12 * c_byte)),
                ("hardwareVersion", c_word),
                ("modificationState", c_word),
                ("numChannels", c_short)]


TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)
# TLI_GetDeviceList  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceList(SAFEARRAY** stringsReceiver);
# TLI_GetDeviceListByType  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID);
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
# TLI_GetDeviceListByTypes  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length);
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)
# TLI_InitializeSimulations
# TLI_UninitializeSimulations


# CC_CanDeviceLockFrontPanel
CC_CanHome = bind(lib, "CC_CanHome", [POINTER(c_char)], c_bool)
# CC_CanMoveWithoutHomingFirst
# CC_CheckConnection
CC_ClearMessageQueue = bind(lib, "CC_ClearMessageQueue", [POINTER(c_char)], None)
CC_Close = bind(lib, "CC_Close", [POINTER(c_char)], None)
# CC_DisableChannel
CC_EnableChannel = bind(lib, "CC_EnableChannel", [POINTER(c_char)], c_short)
# CC_EnableLastMsgTimer
# CC_GetBacklash
# CC_GetDCPIDParams
CC_GetDeviceUnitFromRealValue = bind(lib, "CC_GetDeviceUnitFromRealValue", [POINTER(c_char), c_double, POINTER(c_int), c_int], c_short)
# CC_GetDigitalOutputs
# CC_GetEncoderCounter
# CC_GetFrontPanelLocked
# CC_GetHardwareInfo
# CC_GetHardwareInfoBlock
# CC_GetHomingParamsBlock
# CC_GetHomingVelocity
# CC_GetHubBay
# CC_GetJogMode
# CC_GetJogParamsBlock
CC_GetJogStepSize = bind(lib, "CC_GetJogStepSize", [POINTER(c_char)], c_uint)
CC_GetJogVelParams = bind(lib, "CC_GetJogVelParams", [POINTER(c_char),POINTER(c_int),POINTER(c_int)], c_short)
# CC_GetLEDswitches
# CC_GetLimitSwitchParams
# CC_GetLimitSwitchParamsBlock
# CC_GetMMIParams
# CC_GetMMIParamsBlock
# CC_GetMMIParamsExt
# CC_GetMotorParams
# CC_GetMotorParamsExt
CC_GetMotorTravelLimits = bind(lib, "CC_GetMotorTravelLimits", [POINTER(c_char), POINTER(c_double), POINTER(c_double)], c_short)
# CC_GetMotorTravelMode
# CC_GetMotorVelocityLimits
# CC_GetMoveAbsolutePosition
# CC_GetMoveRelativeDistance
# CC_GetNextMessage
CC_GetNumberPositions = bind(lib, "CC_GetNumberPositions", [POINTER(c_char)], c_int)
CC_GetPosition  = bind(lib, "CC_GetPosition", [POINTER(c_char)], c_int)
# CC_GetPositionCounter
# CC_GetRealValueFromDeviceUnit
# CC_GetSoftLimitMode
# CC_GetSoftwareVersion
# CC_GetStageAxisMaxPos
# CC_GetStageAxisMinPos
CC_GetStatusBits = bind(lib, "CC_GetStatusBits", [POINTER(c_char)], c_dword)
# CC_GetTriggerConfigParams
# CC_GetTriggerConfigParamsBlock
# CC_GetTriggerParamsParams
# CC_GetTriggerParamsParamsBlock
CC_GetVelParams = bind(lib, "CC_GetVelParams", [POINTER(c_char), POINTER(c_int), POINTER(c_int)], c_short)
# CC_GetVelParamsBlock
# CC_HasLastMsgTimerOverrun
CC_Home = bind(lib, "CC_Home", [POINTER(c_char)], c_short)
# CC_Identify
# CC_LoadNamedSettings
CC_LoadSettings = bind(lib, "CC_LoadSettings", [POINTER(c_char)], c_bool)
# CC_MessageQueueSize
# CC_MoveAbsolute
CC_MoveAtVelocity = bind(lib, "CC_MoveAtVelocity", [POINTER(c_char),c_short], c_short)
# CC_MoveJog
CC_MoveJog = bind(lib, "CC_MoveJog", [POINTER(c_char), c_short], c_short)
# CC_MoveRelative
# CC_MoveRelativeDistance
CC_MoveToPosition = bind(lib, "CC_MoveToPosition", [POINTER(c_char),c_int], c_short)
# CC_NeedsHoming
CC_Open = bind(lib, "CC_Open", [POINTER(c_char)], c_short)
# CC_PersistSettings
# CC_PollingDuration
# CC_RegisterMessageCallback
# CC_RequestBacklash
# CC_RequestDCPIDParams
# CC_RequestDigitalOutputs
# CC_RequestEncoderCounter
# CC_RequestFrontPanelLocked
# CC_RequestHomingParams
# CC_RequestJogParams
# CC_RequestLEDswitches
# CC_RequestLimitSwitchParams
# CC_RequestMMIparams
# CC_RequestMoveAbsolutePosition
# CC_RequestMoveRelativeDistance
CC_RequestPosition = bind(lib, "CC_RequestPosition", [POINTER(c_char)], c_short)
# CC_RequestPosTriggerParams
# CC_RequestSettings
CC_RequestSettings = bind(lib, "CC_RequestSettings", [POINTER(c_char)], c_short)
CC_RequestStatusBits = bind(lib, "CC_RequestStatusBits", [POINTER(c_char)], c_short)
# CC_RequestTriggerConfigParams
# CC_RequestVelParams
# CC_ResetRotationModes
# CC_ResetStageToDefaults
# CC_ResumeMoveMessages
# CC_SetBacklash
# CC_SetDCPIDParams
# CC_SetDigitalOutputs
# CC_SetDirection
# CC_SetEncoderCounter
# CC_SetFrontPanelLock
# CC_SetHomingParamsBlock
# CC_SetHomingVelocity
CC_SetJogMode = bind(lib, "CC_SetJogMode", [POINTER(c_char), c_short, c_short], c_short)
# CC_SetJogParamsBlock
CC_SetJogStepSize = bind(lib, "CC_SetJogStepSize", [POINTER(c_char), c_uint], c_short)
# CC_SetJogVelParams
# CC_SetLEDswitches
# CC_SetLimitsSoftwareApproachPolicy
# CC_SetLimitSwitchParams
# CC_SetLimitSwitchParamsBlock
# CC_SetMMIParams
# CC_SetMMIParamsBlock
# CC_SetMMIParamsExt
# CC_SetMotorParams
# CC_SetMotorParamsExt
# CC_SetMotorTravelLimits
# CC_SetMotorTravelMode
# CC_SetMotorVelocityLimits
# CC_SetMoveAbsolutePosition
# CC_SetMoveRelativeDistance
# CC_SetPositionCounter
# CC_SetRotationModes
# CC_SetStageAxisLimits
# CC_SetTriggerConfigParams
# CC_SetTriggerConfigParamsBlock
# CC_SetTriggerParamsParams
# CC_SetTriggerParamsParamsBlock
# CC_SetVelParams
# CC_SetVelParamsBlock
CC_SetVelParams = bind(lib, "CC_SetVelParams", [POINTER(c_char), c_int, c_int], c_short)
CC_StartPolling = bind(lib, "CC_StartPolling", [POINTER(c_char), c_int], c_bool)
CC_StopImmediate = bind(lib, "CC_StopImmediate", [POINTER(c_char)], c_short)
CC_StopPolling = bind(lib, "CC_StopPolling", [POINTER(c_char)], None)
CC_StopProfiled = bind(lib, "CC_StopProfiled",[POINTER(c_char)], c_short)
# CC_SuspendMoveMessages
# CC_TimeSinceLastMsgReceived
CC_WaitForMessage = bind(lib, "CC_WaitForMessage", [POINTER(c_char),POINTER(c_word),POINTER(c_word),POINTER(c_dword)], None)


def is_moving(serialno):
    CC_RequestStatusBits(serialno)
    time.sleep(0.1)
    bits = CC_GetStatusBits(serialno)
    print(bits, type(bits))
    print(bits & 0x00000010)
    print(bits & 0x00000020)
    print(bits & 0x00000040)
    print(bits & 0x00000080)
