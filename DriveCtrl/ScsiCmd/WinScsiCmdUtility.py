from EricCorePy.DriveCtrl.ScsiCmd.WinScsiPassThrough import *
from EricCorePy.DriveCtrl.ScsiCmd.ScsiCmdBase import *


def send_scsi_cmd(handle, cmd: ScsiCmdObj, writeBuffer:bytearray=None):
    if cmd.direct == SCSI_IOCTL_DATA_IN:
        byteArray = bytearray(cmd.dataLen)
    else:
        byteArray = writeBuffer
    scsi_pass_through_direct(handle, cmd.cdb, byteArray, cmd.direct)
    return byteArray

def get_inquiry(handle):
    cmdSet = UfiCmdSet()
    dataBuffer = send_scsi_cmd(handle, cmdSet.inquiry())
    return dataBuffer
