

from .UfiCmdSet import *
from EricCorePy.DriveCtrl.ScsiCmd.ScsiPassThrough import *

class UfiCmd:
    def __init__(self, handle=None):
        self.m_ufi = UfiCmdSet()
        self.m_handle = handle
    
    def get_inquiry(self):
        return send_scsi_cmd(self.m_handle, self.m_ufi.inquiry())
    
    def lba_read(self, lba, secCnt):
        return send_scsi_cmd(self.m_handle, self.m_ufi.read_10(lba, secCnt))
    
    def lba_write(self, lba, secCnt, buffer):
        return send_scsi_cmd(self.m_handle, self.m_ufi.write_10(lba, secCnt), buffer)

    def send_cmd(self, cmd: ScsiCmdBase, writeBuffer=None):
        return send_scsi_cmd(self.m_handle, cmd, writeBuffer)