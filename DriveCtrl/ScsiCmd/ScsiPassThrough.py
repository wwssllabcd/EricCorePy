from EricCorePy.DriveCtrl.ScsiCmd.WinScsiPassThrough import *
from EricCorePy.DriveCtrl.ScsiCmd.ScsiCmdObj import *


def send_scsi_cmd(handle, cmd: ScsiCmdBase, writeBuffer=None):
    if cmd.direct == SCSI_IOCTL_DATA_IN:
        byteArray = bytearray(cmd.dataLen)
    else:
        if type(writeBuffer) == list:
            # check list len for performance issue
            if len(writeBuffer) >= 4096:
                print("conver to bytearray, but list len too big = " + str(len(writeBuffer)))

        # try to convert to bytearray, include list
        byteArray = bytearray(writeBuffer)

    win_scsi_pass_through_direct(handle, cmd.cdb, byteArray, cmd.direct)
    return byteArray

