from EricCorePy.DriveCtrl.ScsiCmd.WinScsiPassThrough import *
from EricCorePy.DriveCtrl.ScsiCmd.ScsiCmdObj import *


def send_scsi_cmd(handle, cmd: ScsiCmdBase, writeBuffer=None):
    if cmd.direct == SCSI_IOCTL_DATA_IN:
        byteArray = bytearray(cmd.dataLen)
    else:
        # try to convert to bytearray, include list
        byteArray = bytearray(writeBuffer)

    win_scsi_pass_through_direct(handle, cmd.cdb, byteArray, cmd.direct)
    return byteArray

