import ctypes
from ctypes import wintypes

IOCTL_SCSI_PASS_THROUGH_DIRECT = 0x4D014
SCSI_IOCTL_DATA_IN = 1
SCSI_IOCTL_DATA_OUT = 0

class SCSI_PASS_THROUGH_DIRECT(ctypes.Structure):
    _fields_ = [
        ("Length", wintypes.USHORT),
        ("ScsiStatus", ctypes.c_ubyte),
        ("PathId", ctypes.c_ubyte),
        ("TargetId", ctypes.c_ubyte),
        ("Lun", ctypes.c_ubyte),
        ("CdbLength", ctypes.c_ubyte),
        ("SenseInfoLength", ctypes.c_ubyte),
        ("DataIn", ctypes.c_ubyte),
        ("DataTransferLength", wintypes.ULONG),
        ("TimeOutValue", wintypes.ULONG),
        ("DataBuffer", ctypes.c_void_p),
        ("SenseInfoOffset", wintypes.ULONG),
        ("Cdb", ctypes.c_ubyte * 16)
    ]

def to_ctype_addr(byteArray):
    data_buffer_ctypes = (ctypes.c_char * len(byteArray)).from_buffer(byteArray)
    return ctypes.addressof(data_buffer_ctypes)

def scsi_pass_through_direct(handle, cdb, byteArray: bytearray, direction=SCSI_IOCTL_DATA_IN, timeout=20):
    sptd = SCSI_PASS_THROUGH_DIRECT()
    sptd.Length = ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT)
    sptd.CdbLength = len(cdb)
    sptd.SenseInfoLength = 0
    sptd.DataIn = direction
    sptd.DataTransferLength = len(byteArray)
    sptd.TimeOutValue = timeout
    
    sptd.DataBuffer = to_ctype_addr(byteArray)
    

    sptd.SenseInfoOffset = 0
    sptd.Cdb[:len(cdb)] = cdb

    bytes_returned = wintypes.DWORD()

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

