from ctypes import c_uint32
from .ScsiCmdDefine import *
from EricCorePy.Utility.CtypeUtility import *

IOCTL_SCSI_PASS_THROUGH_DIRECT = 0x4D014


class SCSI_PASS_THROUGH_DIRECT(ctypes.Structure):
    _fields_ = [
        ("Length", ctypes.c_uint16),
        ("ScsiStatus", ctypes.c_ubyte),
        ("PathId", ctypes.c_ubyte),
        ("TargetId", ctypes.c_ubyte),
        ("Lun", ctypes.c_ubyte),
        ("CdbLength", ctypes.c_ubyte),
        ("SenseInfoLength", ctypes.c_ubyte),
        ("DataIn", ctypes.c_ubyte),
        ("DataTransferLength", ctypes.c_int32),
        ("TimeOutValue", ctypes.c_int32),
        ("DataBuffer", ctypes.c_void_p),
        ("SenseInfoOffset", ctypes.c_int32),
        ("Cdb", ctypes.c_ubyte * 16)
    ]

def win_scsi_pass_through_direct(handle, cdb, byteArray: bytearray, direction=SCSI_IOCTL_DATA_IN, timeout=20):
    sptd = SCSI_PASS_THROUGH_DIRECT()
    sptd.Length = ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT)
    sptd.CdbLength = len(cdb)
    sptd.SenseInfoLength = 0
    sptd.DataIn = direction
    sptd.DataTransferLength = len(byteArray)
    sptd.TimeOutValue = timeout
    
    sptd.DataBuffer = get_ctype_addr(byteArray)

    sptd.SenseInfoOffset = 0
    sptd.Cdb[:len(cdb)] = cdb

    bytes_returned = c_uint32()

    result = ctypes.windll.kernel32.DeviceIoControl(
        handle,
        IOCTL_SCSI_PASS_THROUGH_DIRECT,
        ctypes.byref(sptd),
        ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT),
        ctypes.byref(sptd),
        ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT),
        ctypes.byref(bytes_returned),
        None
    )

    if result == 0:
        raise ctypes.WinError()

    return byteArray

