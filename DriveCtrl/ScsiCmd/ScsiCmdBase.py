
from .ScsiCmdDefine import *
from EricCorePy.Utility.EricUtility import *

class ScsiCmdBase:
    def __init__(self):
        self.cdb = bytearray(16)
        self.dataLen = 0
        self.desc = ""
        self.direct = SCSI_IOCTL_DATA_IN
    
    def __str__(self):
        u = EricUtility()
        res = []
        res.append(u.make_hex_table(self.cdb, 1, True))
        res.append(f"direct = {hex(self.direct)}")
        res.append(f"dataLen = {hex(self.dataLen)}")
        return CRLF.join(res)
