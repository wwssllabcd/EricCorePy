
from .ScsiCmdDefine import *

class ScsiCmdBase:
    def __init__(self):
        self.cdb = [0]*16
        self.dataLen = 0
        self.desc = ""
        self.direct = SCSI_IOCTL_DATA_IN

class UfiCmdSet:
    def get_read_10(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_READ_10
        cmd.cdb[8] = 0x01
        cmd.dataLen = cmd.cdb[8]*BYTE_PER_SECTOR

        cmd.direct = SCSI_IOCTL_DATA_IN
        cmd.desc = "UFI: Read10"
        return cmd

    def get_write_10(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_WRITE_10
        cmd.cdb[8] = 0x01
        cmd.dataLen = cmd.cdb[8]*BYTE_PER_SECTOR
        cmd.desc = "UFI: Write10"
        cmd.direct = SCSI_IOCTL_DATA_OUT
        return cmd

    def inquiry(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_INQUIRY
        cmd.cdb[4] = 0x24
        cmd.dataLen = 0x24
        cmd.desc = "UFI: Inquiry"
        cmd.direct = SCSI_IOCTL_DATA_IN
        return cmd
    
    def ata_pass_through_12(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = SCSI_OP_SAT12
        cmd.desc = "SCSI: ata_pass_through_12"
        cmd.direct = SCSI_IOCTL_NON_DATA
        return cmd

    def get_cmd_colls(self):
        cmdColl = [self.inquiry(), self.get_write_10(), self.get_read_10(),  self.ata_pass_through_12()]
        return cmdColl
