# Bindings for Thorlabs Benchtop Piezo BCP 303 (3 channel piezo controller)
# Implemented with Kinesis Version 1.14.23.16838
import thorlabs_kinesis as tk

# import c types
from ctypes import (
    Structure,
    cdll,
    c_bool,
    c_short,
    c_uint,
    c_int,
    c_int32,
    c_int64,
    c_char,
    c_byte,
    c_long,
    POINTER,
)

from thorlabs_kinesis._utils import (
    c_word,
    c_dword,
    bind
)

lib = cdll.LoadLibrary("Thorlabs.MotionControl.Benchtop.Piezo.dll")


# enum MOT_MotorTypes (c_int)
MOT_NotMotor = c_int(0)
MOT_DCMotor = c_int(1)
MOT_StepperMotor = c_int(2)
MOT_BrushlessMotor = c_int(3)
MOT_CustomMotor = c_int(100)
MOT_MotorTypes = c_int

# enum control types (c_int)
PZ_Undefined = c_short(0)
PZ_OpenLoop = c_short(1)
PZ_ClosedLoop = c_short(2)
PZ_OpenLoopSmoothed = c_short(3)
PZ_ClosedLoopSmoothed = c_short(4)
PZ_ControlModeTypes = c_short # this is the variable the int will be saved to

# enum PZ_InputSourceFlags # TODO: Verify these!
PZ_SoftwareOnly = c_short(0)
PZ_ExternalSignal = c_short(1)
PZ_Potentiometer = c_short(2)
PZ_All = c_short(3)
PZ_InputSourceFlags = c_short

# enum PZ_OutputLUTModes
PZ_Continuous = c_short(0)
PZ_Fixed = c_short(1)
PZ_OutputTrigEnable = c_short(2)
PZ_InputTrigEnable = c_short(3)
PZ_OutputTrigSenseHigh = c_short(4)
PZ_InputTrigSenseHigh = c_short(5)
PZ_OutputGated = c_short(6)
PZ_OutputTrigRepeat = c_short(7)
PZ_OutputLUTModes = c_short


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

class PZ_FeedbackLoopConstants(Structure):
    _fields_ = [("integralTerm", c_short),
                ("proportionalTerm", c_short)]

class PZ_LUTWaveParameters(Structure):
    _fields_ = [("cycleLength", c_short),
                ("LUTValueDelay", c_uint),
                ("mode", PZ_OutputLUTModes),
                ("numCycles", c_uint),
                ("numOutTriggerRepeat", c_short),
                ("outTriggerDuration", c_uint),
                ("outTriggerStart", c_short),
                ("postCycleDelay", c_uint),
                ("preCycleDelay", c_uint)]


TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)
# TLI_GetDeviceList  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceList(SAFEARRAY** stringsReceiver);
# TLI_GetDeviceListByType  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID);
# TLI_GetDeviceListByTypes  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length);
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)

PBC_CheckConnection = bind(lib, "PBC_CheckConnection", [POINTER(c_char)], c_bool)
PBC_ClearMessageQueue = bind(lib, "PBC_ClearMessageQueue", [POINTER(c_char)], c_short)
PBC_Close = bind(lib, "PBC_Close", [POINTER(c_char)], None)
PBC_DisableChannel = bind(lib, "PBC_DisableChannel", [POINTER(c_char), c_short], c_short)
PBC_Disconnect = bind(lib, "PBC_Disconnect", [POINTER(c_char)], c_short) 
PBC_EnableChannel = bind(lib, "PBC_EnableChannel", [POINTER(c_char), c_short], c_short)
PBC_EnableLastMsgTimer = bind(lib, "PBC_EnableLastMsgTimer", [POINTER(c_char), c_short, c_bool, c_int32], None)
PBC_GetFeedbackLoopPIconsts = bind(lib, "PBC_GetFeedbackLoopPIconsts", [POINTER(c_char), c_short, POINTER(c_short), POINTER(c_short)], c_short)
PBC_GetFeedbackLoopPIconstsBlock = bind(lib, "PBC_GetFeedbackLoopPIconstsBlock", [POINTER(c_char), c_short, POINTER(PZ_FeedbackLoopConstants)], c_short)
PBC_GetFirmwareVersion = bind(lib, "PBC_GetFirmwareVersion", [POINTER(c_char)], c_dword)
PBC_GetHardwareInfo = bind(lib, "PBC_GetHardwareInfo", [POINTER(c_char), c_short, POINTER(c_char), c_dword, POINTER(c_word), POINTER(c_word), POINTER(c_char), c_dword, POINTER(c_dword), POINTER(c_word), POINTER(c_word)], c_short)
PBC_GetHardwareInfoBlock = bind(lib, "PBC_GetHardwareInfoBlock", [POINTER(c_char), c_short, TLI_HardwareInformation], c_short)
PBC_GetMaximumTravel = bind(lib, "PBC_GetMaximumTravel", [POINTER(c_char),  c_short], c_short)
PBC_GetMaxOutputVoltage = bind(lib, "PBC_GetMaxOutputVoltage", [POINTER(c_char), c_short], c_short)
PBC_GetNextMessage = bind(lib, "PBC_GetNextMessage", [POINTER(c_char), c_short, POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool)
PBC_GetNumChannels = bind(lib, "PBC_GetNumChannels", [POINTER(c_char)], c_short)
PBC_GetOutputVoltage = bind(lib, "PBC_GetOutputVoltage", [POINTER(c_char), c_short], c_short)
PBC_GetPosition = bind(lib, "PBC_GetPosition", [POINTER(c_char), c_short], c_short)
PBC_GetPositionControlMode = bind(lib, "PBC_GetPositionControlMode", [POINTER(c_char), c_short], PZ_ControlModeTypes)
PBC_GetRackDigitalOutputs = bind(lib, "PBC_GetRackDigitalOutputs", [POINTER(c_char)], c_byte)
PBC_GetRackStatusBits = bind(lib, "PBC_GetRackStatusBits", [POINTER(c_char)], c_dword)
PBC_GetSoftwareVersion = bind(lib, "PBC_GetSoftwareVersion", [POINTER(c_char)], c_dword)
PBC_GetStatusBits = bind(lib, "PBC_GetStatusBits", [POINTER(c_char), c_short], c_dword)
PBC_GetVoltageSource = bind(lib, "PBC_GetVoltageSource", [POINTER(c_char), c_short], PZ_InputSourceFlags)
PBC_HasLastMsgTimerOverrun = bind(lib, "PBC_HasLastMsgTimerOverrun", [POINTER(c_char), c_short], c_bool)
PBC_Identify = bind(lib, "PBC_Identify", [POINTER(c_char), c_short], None)
PBC_IsChannelValid = bind(lib, "PBC_IsChannelValid", [POINTER(c_char), c_short], c_bool)
PBC_LoadNamedSettings = bind(lib, "PBC_LoadNamedSettings", [POINTER(c_char), c_short, POINTER(c_char)], c_bool)
PBC_LoadSettings = bind(lib, "PBC_LoadSettings", [POINTER(c_char), c_short], c_bool)
PBC_MaxChannelCount = bind(lib, "PBC_MaxChannelCount", [POINTER(c_char)], c_int)
PBC_MessageQueueSize = bind(lib, "PBC_MessageQueueSize", [POINTER(c_char), c_short], c_int)
PBC_Open = bind(lib, "PBC_Open", [POINTER(c_char)], c_short)
PBC_PersistSettings = bind(lib, "PBC_PersistSettings", [POINTER(c_char), c_short], c_bool)
PBC_PollingDuration = bind(lib, "PBC_PollingDuration", [POINTER(c_char), c_short], c_long)
# PBC_RegisterMessageCallback = 
PBC_RequestActualPosition = bind(lib, "PBC_RequestActualPosition", [POINTER(c_char), c_short], c_short)
PBC_RequestFeedbackLoopPIconsts = bind(lib, "PBC_RequestFeedbackLoopPIconsts", [POINTER(c_char), c_short], c_bool)
PBC_RequestMaximumTravel = bind(lib, "PBC_RequestMaximumTravel", [POINTER(c_char), c_short], c_bool)
PBC_RequestMaxOutputVoltage = bind(lib, "PBC_RequestMaxOutputVoltage", [POINTER(c_char), c_short], c_bool)
PBC_RequestOutputVoltage = bind(lib, "PBC_RequestOutputVoltage", [POINTER(c_char), c_short], c_bool)
PBC_RequestPosition = bind(lib, "PBC_RequestPosition", [POINTER(c_char), c_short], c_short)
PBC_RequestPositionControlMode = bind(lib, "PBC_RequestPositionControlMode", [POINTER(c_char), c_short], c_bool)
PBC_RequestRackDigitalOutputs = bind(lib, "PBC_RequestRackDigitalOutputs", [POINTER(c_char)], c_short)
PBC_RequestRackStatusBits = bind(lib, "PBC_RequestRackStatusBits", [POINTER(c_char)], c_short)
PBC_RequestSettings = bind(lib, "PBC_RequestSettings", [POINTER(c_char), c_short], c_short)
PBC_RequestStatus = bind(lib, "PBC_RequestStatus", [POINTER(c_char), c_short], c_short)
PBC_RequestStatusBits = bind(lib, "PBC_RequestStatusBits", [POINTER(c_char), c_short], c_short)
PBC_RequestVoltageSource = bind(lib, "PBC_RequestVoltageSource", [POINTER(c_char), c_short], c_bool)
PBC_ResetParameters = bind(lib, "PBC_ResetParameters", [POINTER(c_char), c_short], c_short)
PBC_SetFeedbackLoopPIconsts = bind(lib, "PBC_SetFeedbackLoopPIconsts", [POINTER(c_char), c_short, c_short, c_short], c_bool)
PBC_SetFeedbackLoopPIconstsBlock = bind(lib, "PBC_SetFeedbackLoopPIconstsBlock", [POINTER(c_char), c_short, POINTER(PZ_FeedbackLoopConstants)], c_short)
PBC_SetLUTwaveParams = bind(lib, "PBC_SetLUTwaveParams", [POINTER(c_char), c_short, POINTER(PZ_LUTWaveParameters)], c_short)
PBC_SetLUTwaveSample = bind(lib, "PBC_SetLUTwaveSample", [POINTER(c_char), c_short, c_short, c_word], c_short)
PBC_SetMaxOutputVoltage = bind(lib, "PBC_SetMaxOutputVoltage", [POINTER(c_char), c_short, c_short], c_short)
PBC_SetOutputVoltage = bind(lib, "PBC_SetOutputVoltage", [POINTER(c_char), c_short, c_short], c_short)
PBC_SetPosition = bind(lib, "PBC_SetPosition", [POINTER(c_char), c_short, c_short], c_short)
PBC_SetPositionControlMode = bind(lib, "PBC_SetPositionControlMode", [POINTER(c_char), c_short, PZ_ControlModeTypes], c_short)
PBC_SetPositionToTolerance = bind(lib, "PBC_SetPositionToTolerance", [POINTER(c_char), c_short, c_short, c_short], c_short)
PBC_SetRackDigitalOutputs = bind(lib, "PBC_SetRackDigitalOutputs", [POINTER(c_char), c_byte], c_short)
PBC_SetVoltageSource = bind(lib, "PBC_SetVoltageSource", [POINTER(c_char), c_short, PZ_InputSourceFlags], c_short)
PBC_SetZero = bind(lib, "PBC_SetZero", [POINTER(c_char), c_short], c_short)
PBC_StartLUTwave = bind(lib, "PBC_StartLUTwave", [POINTER(c_char), c_short], c_short)
PBC_StartPolling = bind(lib, "PBC_StartPolling", [POINTER(c_char), c_short, c_int], c_bool)
PBC_StopLUTwave = bind(lib, "PBC_StopLUTwave", [POINTER(c_char), c_short], c_short)
PBC_StopPolling = bind(lib, "PBC_StopPolling", [POINTER(c_char), c_short], None)
PBC_TimeSinceLastMsgReceived = bind(lib, "", [POINTER(c_char), c_short, POINTER(c_int64)], c_bool)
PBC_WaitForMessage = bind(lib, "PBC_WaitForMessage", [POINTER(c_char), c_short, POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool)
