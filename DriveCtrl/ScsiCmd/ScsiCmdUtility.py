

from .ScsiCmdObj import *
from EricCorePy.DriveCtrl.ScsiCmd.ScsiPassThrough import *

class ScsiCmdUtility:
    def __init__(self, handle=None):
        self.m_ufi = UfiCmdSet()
        self.m_handle = handle
    
    def get_inquiry(self):
        return send_scsi_cmd(self.m_handle, self.m_ufi.inquiry())

