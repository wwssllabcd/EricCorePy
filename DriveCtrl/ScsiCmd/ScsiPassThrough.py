from EricCorePy.DriveCtrl.ScsiCmd.WinScsiPassThrough import *
from EricCorePy.DriveCtrl.ScsiCmd.ScsiCmdObj import *


def send_scsi_cmd(handle, cmd: ScsiCmdBase, writeBuffer:bytearray=None):
    if cmd.direct == SCSI_IOCTL_DATA_IN:
        byteArray = bytearray(cmd.dataLen)
    else:
        byteArray = writeBuffer
    win_scsi_pass_through_direct(handle, cmd.cdb, byteArray, cmd.direct)
    return byteArray

