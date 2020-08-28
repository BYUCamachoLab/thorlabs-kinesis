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
    bind,
    not_implemented,
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
MOT_TravelDirectionDisabled = c_short(0x00)
MOT_Forwards = c_short(0x01)
MOT_Reverse = c_short(0x02)
MOT_TravelDirection = c_short

# enum MOT_JogModes
MOT_JogModeUndefined = c_short(0x00)
MOT_Continuous = c_short(0x01)
MOT_SingleStep = c_short(0x02)
MOT_JogModes = c_short

# enum MOT_StopModes
MOT_StopModeUndefined = c_short(0x00)
MOT_Immediate = c_short(0x01)
MOT_Profiled = c_short(0x02)
MOT_StopModes = c_short

# enum MOT_TravelModes
MOT_TravelModeUndefined = c_int(0)
MOT_Linear = c_int(1)
MOT_Rotational = c_int(2)
MOT_TravelModes = c_int

# enum MOT_LimitsSoftwareApproachPolicy
DisallowIllegalMoves = c_short(0x00)
AllowPartialMoves = c_short(0x01)
AllowAllMoves = c_short(0x02)
MOT_LimitsSoftwareApproachPolicy = c_short

# enum MOT_HomeLimitSwitchDirection
MOT_LimitSwitchDirectionUndefined = c_short(0x00)
MOT_ReverseLimitSwitch = c_short(0x01)
MOT_ForwardLimitSwitch = c_short(0x02)
MOT_HomeLimitSwitchDirection = c_short

# enum MOT_LimitSwitchModes
MOT_LimitSwitchModeUndefined = c_word(0x00)
MOT_LimitSwitchIgnoreSwitch = c_word(0x01)
MOT_LimitSwitchMakeOnContact = c_word(0x02)
MOT_LimitSwitchBreakOnContact = c_word(0x03)
MOT_LimitSwitchMakeOnHome = c_word(0x04)
MOT_LimitSwitchBreakOnHome = c_word(0x05)
MOT_PMD_Reserved = c_word(0x06)
MOT_LimitSwitchIgnoreSwitchSwapped = c_word(0x81)
MOT_LimitSwitchMakeOnContactSwapped = c_word(0x82)
MOT_LimitSwitchBreakOnContactSwapped = c_word(0x83)
MOT_LimitSwitchMakeOnHomeSwapped = c_word(0x84)
MOT_LimitSwitchBreakOnHomeSwapped = c_word(0x85)
MOT_LimitSwitchModes = c_word

# enum MOT_LimitSwitchSWModes
MOT_LimitSwitchSWModeUndefined = c_word(0)
MOT_LimitSwitchIgnored = c_word(1)
MOT_LimitSwitchStopImmediate = c_word(2)
MOT_LimitSwitchStopProfiled = c_word(3)
MOT_LimitSwitchIgnored_Rotational = c_word(4)
MOT_LimitSwitchStopImmediate_Rotational = c_word(5)
MOT_LimitSwitchStopProfiled_Rotational = c_word(6)
MOT_LimitSwitchSWModes = c_word

# enum MOT_MovementModes
LinearRange = c_int(0x00)
RotationalUnlimited = c_int(0x01)
RotationalWrapping = c_int(0x02)
MOT_MovementModes = c_int

# enum MOT_MovementDirections
Quickest = c_int(0x00)
Forwards = c_int(0x01)
Reverse = c_int(0x02)
MOT_MovementDirections = c_int


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

class MOT_HomingParameters(Structure):
    _fields_ = [("direction", MOT_TravelDirection),
                ("limitSwitch", MOT_HomeLimitSwitchDirection),
                ("offsetDistance", c_uint),
                ("velocity", c_uint)]

class MOT_VelocityParameters(Structure):
    _fields_ = [("acceleration", c_int),
                ("maxVelocity", c_int),
                ("minVelocity", c_int)]

class MOT_JogParameters(Structure):
    _fields_ = [("mode", MOT_JogModes),
                ("stepSize", c_uint),
                ("stopMode", MOT_StopModes),
                ("velParams", MOT_VelocityParameters)]

class MOT_DC_PIDParameters(Structure):
    _fields_ = [("differentialGain", c_int),
                ("integralGain", c_int),
                ("integralLimit", c_int),
                ("parameterFilter", c_word),
                ("proportionalGain", c_int)]

class MOT_LimitSwitchParameters(Structure):
    _fields_ = [("anticlockwiseHardwareLimit", MOT_LimitSwitchModes),
                ("anticlockwisePosition", c_dword),
                ("clockwiseHardwareLimit", MOT_LimitSwitchModes),
                ("clockwisePosition", c_dword),
                ("softLimitMode", MOT_LimitSwitchSWModes)]


TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)
TLI_GetDeviceList = not_implemented # <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceList(SAFEARRAY** stringsReceiver);
TLI_GetDeviceListByType = not_implemented # <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID);
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
TLI_GetDeviceListByTypes = not_implemented # <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length);
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)
TLI_InitializeSimulations = not_implemented
TLI_UninitializeSimulations = not_implemented


CC_CanDeviceLockFrontPanel = bind(lib, "CC_CanDeviceLockFrontPanel", [POINTER(c_char)], c_bool)
CC_CanHome = bind(lib, "CC_CanHome", [POINTER(c_char)], c_bool)
CC_CanMoveWithoutHomingFirst = bind(lib, "CC_CanMoveWithoutHomingFirst", [POINTER(c_char)], c_bool)
CC_CheckConnection = bind(lib, "CC_CheckConnection", [POINTER(c_char)], c_bool)
CC_ClearMessageQueue = bind(lib, "CC_ClearMessageQueue", [POINTER(c_char)], None)
CC_Close = bind(lib, "CC_Close", [POINTER(c_char)], None)
CC_DisableChannel = bind(lib, "CC_DisableChannel", [POINTER(c_char)], c_short)
CC_EnableChannel = bind(lib, "CC_EnableChannel", [POINTER(c_char)], c_short)
CC_EnableLastMsgTimer = bind(lib, "CC_EnableLastMsgTimer", [POINTER(c_char), c_bool, c_int32], None)
CC_GetBacklash = bind(lib, "CC_GetBacklash", [POINTER(c_char)], c_long)
CC_GetDCPIDParams = not_implemented # bind(lib, "CC_GetDCPIDParams", [POINTER(c_char), <SOME TYPE OF STRUCTURE HERE>], c_short)
CC_GetDeviceUnitFromRealValue = bind(lib, "CC_GetDeviceUnitFromRealValue", [POINTER(c_char), c_double, POINTER(c_int), c_int], c_short)
CC_GetDigitalOutputs = bind(lib, "CC_GetDigitalOutputs", [POINTER(c_char)], c_byte)
CC_GetEncoderCounter = bind(lib, "CC_GetEncoderCounter", [POINTER(c_char)], c_long)
CC_GetFrontPanelLocked = bind(lib, "CC_GetFrontPanelLocked", [POINTER(c_char)], c_bool)
CC_GetHardwareInfo = bind(lib, "CC_GetHardwareInfo", [POINTER(c_char), POINTER(c_char), c_dword, POINTER(c_word), POINTER(c_word), POINTER(c_char), c_dword, POINTER(c_dword), POINTER(c_word), POINTER(c_word)], c_short)
CC_GetHardwareInfoBlock = bind(lib, "CC_GetHardwareInfoBlock", [POINTER(c_char), POINTER(TLI_HardwareInformation)], c_short)
CC_GetHomingParamsBlock = bind(lib, "CC_GetHomingParamsBlock", [POINTER(c_char), POINTER(MOT_HomingParameters)], c_short)
CC_GetHomingVelocity = bind(lib, "CC_GetHomingVelocity", [POINTER(c_char)], c_uint)
CC_GetHubBay = bind(lib, "CC_GetHubBay", [POINTER(c_char)], c_char)
CC_GetJogMode = bind(lib, "CC_GetJogMode", [POINTER(c_char), POINTER(MOT_JogModes), POINTER(MOT_StopModes)], c_short)
CC_GetJogParamsBlock = bind(lib, "CC_GetJogParamsBlock", [POINTER(c_char), POINTER(MOT_JogParameters)], c_short)
CC_GetJogStepSize = bind(lib, "CC_GetJogStepSize", [POINTER(c_char)], c_uint)
CC_GetJogVelParams = bind(lib, "CC_GetJogVelParams", [POINTER(c_char), POINTER(c_int), POINTER(c_int)], c_short)
CC_GetLEDswitches = bind(lib, "CC_GetLEDswitches", [POINTER(c_char)], c_word)
CC_GetLimitSwitchParams = bind(lib, "CC_GetLimitSwitchParams", [POINTER(c_char), POINTER(MOT_LimitSwitchModes), POINTER(MOT_LimitSwitchModes), c_uint, c_uint, POINTER(MOT_LimitSwitchSWModes)], c_short)
CC_GetLimitSwitchParamsBlock = bind(lib, "CC_GetLimitSwitchParamsBlock", [POINTER(c_char), POINTER(MOT_LimitSwitchParameters)], c_short)
CC_GetMMIParams = not_implemented # bind(lib, "CC_GetMMIParams", [], )
CC_GetMMIParamsBlock = not_implemented # bind(lib, "CC_GetMMIParamsBlock", [], )
CC_GetMMIParamsExt = not_implemented # bind(lib, "CC_GetMMIParamsExt", [], )
CC_GetMotorParams = bind(lib, "CC_GetMotorParams", [POINTER(c_char), POINTER(c_long), POINTER(c_long), POINTER(c_float)], c_short)
CC_GetMotorParamsExt = bind(lib, "CC_GetMotorParamsExt", [POINTER(c_char), POINTER(c_double), POINTER(c_double), POINTER(c_double)], c_short)
CC_GetMotorTravelLimits = bind(lib, "CC_GetMotorTravelLimits", [POINTER(c_char), POINTER(c_double), POINTER(c_double)], c_short)
CC_GetMotorTravelMode = bind(lib, "CC_GetMotorTravelMode", [POINTER(c_char)], MOT_TravelModes)
CC_GetMotorVelocityLimits = bind(lib, "CC_GetMotorVelocityLimits", [POINTER(c_char), POINTER(c_double), POINTER(c_double)], c_short)
CC_GetMoveAbsolutePosition = bind(lib, "CC_GetMoveAbsolutePosition", [POINTER(c_char)], c_int)
CC_GetMoveRelativeDistance = bind(lib, "CC_GetMoveRelativeDistance", [POINTER(c_char)], c_int)
CC_GetNextMessage = bind(lib, "CC_GetNextMessage", [POINTER(c_char), POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool)
CC_GetNumberPositions = bind(lib, "CC_GetNumberPositions", [POINTER(c_char)], c_int)
CC_GetPosition  = bind(lib, "CC_GetPosition", [POINTER(c_char)], c_int)
CC_GetPositionCounter = bind(lib, "CC_GetPositionCounter", [POINTER(c_char)], c_long)
CC_GetRealValueFromDeviceUnit = bind(lib, "CC_GetRealValueFromDeviceUnit", [POINTER(c_char), c_int, POINTER(c_double), c_int], c_short)
CC_GetSoftLimitMode = bind(lib, "CC_GetSoftLimitMode", [POINTER(c_char)], MOT_LimitsSoftwareApproachPolicy)
CC_GetSoftwareVersion = bind(lib, "CC_GetSoftwareVersion", [POINTER(c_char)], c_dword)
CC_GetStageAxisMaxPos = bind(lib, "CC_GetStageAxisMaxPos", [POINTER(c_char)], c_int)
CC_GetStageAxisMinPos = bind(lib, "CC_GetStageAxisMinPos", [POINTER(c_char)], c_int)
CC_GetStatusBits = bind(lib, "CC_GetStatusBits", [POINTER(c_char)], c_dword)
CC_GetTriggerConfigParams = not_implemented # bind(lib, "CC_GetTriggerConfigParams", [], )
CC_GetTriggerConfigParamsBlock = not_implemented # bind(lib, "CC_GetTriggerConfigParamsBlock", [], )
CC_GetTriggerParamsParams = bind(lib, "CC_GetTriggerParamsParams", [POINTER(c_char), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32)], c_short)
CC_GetTriggerParamsParamsBlock = not_implemented # bind(lib, "CC_GetTriggerParamsParamsBlock", [], )
CC_GetVelParams = bind(lib, "CC_GetVelParams", [POINTER(c_char), POINTER(c_int), POINTER(c_int)], c_short)
CC_GetVelParamsBlock = bind(lib, "CC_GetVelParamsBlock", [POINTER(c_char), POINTER(MOT_VelocityParameters)], c_short)
CC_HasLastMsgTimerOverrun = bind(lib, "CC_HasLastMsgTimerOverrun", [POINTER(c_char)], c_bool)
CC_Home = bind(lib, "CC_Home", [POINTER(c_char)], c_short)
CC_Identify = bind(lib, "CC_Identify", [POINTER(c_char)], None)
CC_LoadNamedSettings = bind(lib, "CC_LoadNamedSettings", [POINTER(c_char), POINTER(c_char)], c_bool)
CC_LoadSettings = bind(lib, "CC_LoadSettings", [POINTER(c_char)], c_bool)
CC_MessageQueueSize = bind(lib, "CC_MessageQueueSize", [POINTER(c_char)], c_int)
CC_MoveAbsolute = bind(lib, "CC_MoveAbsolute", [POINTER(c_char)], c_short)
CC_MoveAtVelocity = bind(lib, "CC_MoveAtVelocity", [POINTER(c_char),c_short], c_short)
CC_MoveJog = bind(lib, "CC_MoveJog", [POINTER(c_char), MOT_TravelDirection], c_short)
CC_MoveRelative = bind(lib, "CC_MoveRelative", [POINTER(c_char), c_int], c_short)
CC_MoveRelativeDistance = bind(lib, "CC_MoveRelativeDistance", [POINTER(c_char)], c_short)
CC_MoveToPosition = bind(lib, "CC_MoveToPosition", [POINTER(c_char),c_int], c_short)
CC_NeedsHoming = bind(lib, "CC_NeedsHoming", [POINTER(c_char)], c_bool)
CC_Open = bind(lib, "CC_Open", [POINTER(c_char)], c_short)
CC_PersistSettings = bind(lib, "CC_PersistSettings", [POINTER(c_char)], c_bool)
CC_PollingDuration = bind(lib, "CC_PollingDuration", [POINTER(c_char)], c_long)
CC_RegisterMessageCallback = not_implemented # bind(lib, "CC_RegisterMessageCallback", [POINTER(c_char), FUNCTION_POINTER?], )
CC_RequestBacklash = bind(lib, "CC_RequestBacklash", [POINTER(c_char)], c_short)
CC_RequestDCPIDParams = bind(lib, "CC_RequestDCPIDParams", [POINTER(c_char)], c_short)
CC_RequestDigitalOutputs = bind(lib, "CC_RequestDigitalOutputs", [POINTER(c_char)], c_short)
CC_RequestEncoderCounter = bind(lib, "CC_RequestEncoderCounter", [POINTER(c_char)], c_short)
CC_RequestFrontPanelLocked = bind(lib, "CC_RequestFrontPanelLocked", [POINTER(c_char)], c_short)
CC_RequestHomingParams = bind(lib, "CC_RequestHomingParams", [POINTER(c_char)], c_short)
CC_RequestJogParams = bind(lib, "CC_RequestJogParams", [POINTER(c_char)], c_short)
CC_RequestLEDswitches = bind(lib, "CC_RequestLEDswitches", [POINTER(c_char)], c_short)
CC_RequestLimitSwitchParams = bind(lib, "CC_RequestLimitSwitchParams", [POINTER(c_char)], c_short)
CC_RequestMMIparams = bind(lib, "CC_RequestMMIparams", [POINTER(c_char)], c_short)
CC_RequestMoveAbsolutePosition = bind(lib, "CC_RequestMoveAbsolutePosition", [POINTER(c_char)], c_short)
CC_RequestMoveRelativeDistance = bind(lib, "CC_RequestMoveRelativeDistance", [POINTER(c_char)], c_short)
CC_RequestPosition = bind(lib, "CC_RequestPosition", [POINTER(c_char)], c_short)
CC_RequestPosTriggerParams = bind(lib, "CC_RequestPosTriggerParams", [POINTER(c_char)], c_short)
CC_RequestSettings = bind(lib, "CC_RequestSettings", [POINTER(c_char)], c_short)
CC_RequestSettings = bind(lib, "CC_RequestSettings", [POINTER(c_char)], c_short)
CC_RequestStatusBits = bind(lib, "CC_RequestStatusBits", [POINTER(c_char)], c_short)
CC_RequestTriggerConfigParams = bind(lib, "CC_RequestTriggerConfigParams", [POINTER(c_char)], c_short)
CC_RequestVelParams = bind(lib, "CC_RequestVelParams", [POINTER(c_char)], c_short)
CC_ResetRotationModes = bind(lib, "CC_ResetRotationModes", [POINTER(c_char)], c_short)
CC_ResetStageToDefaults = bind(lib, "CC_ResetStageToDefaults", [POINTER(c_char)], c_short)
CC_ResumeMoveMessages = bind(lib, "CC_ResumeMoveMessages", [POINTER(c_char)], c_short)
CC_SetBacklash = bind(lib, "CC_SetBacklash", [POINTER(c_char), c_long], c_short)
CC_SetDCPIDParams = bind(lib, "CC_SetDCPIDParams", [POINTER(c_char), POINTER(MOT_DC_PIDParameters)], c_short)
CC_SetDigitalOutputs = bind(lib, "CC_SetDigitalOutputs", [POINTER(c_char), c_byte], c_short)
CC_SetDirection = bind(lib, "CC_SetDirection", [POINTER(c_char), c_bool], None)
CC_SetEncoderCounter = bind(lib, "CC_SetEncoderCounter", [POINTER(c_char), c_long], c_short)
CC_SetFrontPanelLock = bind(lib, "CC_SetFrontPanelLock", [POINTER(c_char), c_bool], c_short)
CC_SetHomingParamsBlock = bind(lib, "CC_SetHomingParamsBlock", [POINTER(c_char), POINTER(MOT_HomingParameters)], c_short)
CC_SetHomingVelocity = bind(lib, "CC_SetHomingVelocity", [POINTER(c_char), c_uint], c_short)
CC_SetJogMode = bind(lib, "CC_SetJogMode", [POINTER(c_char), c_short, c_short], c_short)
CC_SetJogParamsBlock = bind(lib, "CC_SetJogParamsBlock", [POINTER(c_char), POINTER(MOT_JogParameters)], c_short)
CC_SetJogStepSize = bind(lib, "CC_SetJogStepSize", [POINTER(c_char), c_uint], c_short)
CC_SetJogVelParams = bind(lib, "CC_SetJogVelParams", [POINTER(c_char), c_int, c_int], c_short)
CC_SetLEDswitches = bind(lib, "CC_SetLEDswitches", [POINTER(c_char), c_word], c_short)
CC_SetLimitsSoftwareApproachPolicy = bind(lib, "CC_SetLimitsSoftwareApproachPolicy", [POINTER(c_char), MOT_LimitsSoftwareApproachPolicy], None)
CC_SetLimitSwitchParams = bind(lib, "CC_SetLimitSwitchParams", [POINTER(c_char), MOT_LimitSwitchModes, MOT_LimitSwitchModes, c_uint, c_uint, MOT_LimitSwitchSWModes], c_short)
CC_SetLimitSwitchParamsBlock = bind(lib, "CC_SetLimitSwitchParamsBlock", [POINTER(c_char), POINTER(MOT_LimitSwitchParameters)], c_short)
CC_SetMMIParams = not_implemented # bind(lib, "CC_SetMMIParams", [], )
CC_SetMMIParamsBlock = not_implemented # bind(lib, "CC_SetMMIParamsBlock", [], )
CC_SetMMIParamsExt = not_implemented # bind(lib, "CC_SetMMIParamsExt", [], )
CC_SetMotorParams = bind(lib, "CC_SetMotorParams", [POINTER(c_char), c_long, c_long, c_float], c_short)
CC_SetMotorParamsExt = bind(lib, "CC_SetMotorParamsExt", [POINTER(c_char), c_double, c_double, c_double], c_short)
CC_SetMotorTravelLimits = bind(lib, "CC_SetMotorTravelLimits", [POINTER(c_char), c_double, c_double], c_short)
CC_SetMotorTravelMode = bind(lib, "CC_SetMotorTravelMode", [POINTER(c_char), MOT_TravelModes], c_short)
CC_SetMotorVelocityLimits = bind(lib, "CC_SetMotorVelocityLimits", [POINTER(c_char), c_double, c_double], c_short)
CC_SetMoveAbsolutePosition = bind(lib, "CC_SetMoveAbsolutePosition", [POINTER(c_char), c_int], c_short)
CC_SetMoveRelativeDistance = bind(lib, "CC_SetMoveRelativeDistance", [POINTER(c_char), c_int], c_short)
CC_SetPositionCounter = bind(lib, "CC_SetPositionCounter", [POINTER(c_char), c_long], c_short)
CC_SetRotationModes = bind(lib, "CC_SetRotationModes", [POINTER(c_char), MOT_MovementModes, MOT_MovementDirections], c_short)
CC_SetStageAxisLimits = bind(lib, "CC_SetStageAxisLimits", [POINTER(c_char), c_int, c_int], c_short)
CC_SetTriggerConfigParams = not_implemented # bind(lib, "CC_SetTriggerConfigParams", [], )
CC_SetTriggerConfigParamsBlock = not_implemented # bind(lib, "CC_SetTriggerConfigParamsBlock", [], )
CC_SetTriggerParamsParams = not_implemented # bind(lib, "CC_SetTriggerParamsParams", [], )
CC_SetTriggerParamsParamsBlock = not_implemented # bind(lib, "CC_SetTriggerParamsParamsBlock", [], )
CC_SetVelParams = bind(lib, "CC_SetVelParams", [POINTER(c_char), c_int, c_int], c_short)
CC_SetVelParamsBlock = bind(lib, "CC_SetVelParamsBlock", [POINTER(c_char), POINTER(MOT_VelocityParameters)], c_short)
CC_StartPolling = bind(lib, "CC_StartPolling", [POINTER(c_char), c_int], c_bool)
CC_StopImmediate = bind(lib, "CC_StopImmediate", [POINTER(c_char)], c_short)
CC_StopPolling = bind(lib, "CC_StopPolling", [POINTER(c_char)], None)
CC_StopProfiled = bind(lib, "CC_StopProfiled",[POINTER(c_char)], c_short)
CC_SuspendMoveMessages = bind(lib, "CC_SuspendMoveMessages", [POINTER(c_char)], c_short)
CC_TimeSinceLastMsgReceived = not_implemented # bind(lib, "CC_TimeSinceLastMsgReceived", [POINTER(c_char)], )
CC_WaitForMessage = bind(lib, "CC_WaitForMessage", [POINTER(c_char),POINTER(c_word),POINTER(c_word),POINTER(c_dword)], None)
