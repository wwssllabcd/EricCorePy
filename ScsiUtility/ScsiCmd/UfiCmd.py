
from .ScsiCmdObj import *


class UfiCmdSet:
    def get_read_10(self):
        cmd = ScsiCmdObj()
        cmd.cdb[0] = 0x28
        cmd.cdb[8] = 0x01
        cmd.len = cmd.cdb[8]*512

        cmd.direct = SCS_DATA_IN
        cmd.desc = "UFI: Read10"
        return cmd

    def get_write_10(self):
        cmd = ScsiCmdObj()
        cmd.cdb[0] = 0x2A
        cmd.cdb[8] = 0x01
        cmd.len = cmd.cdb[8]*512
        cmd.desc = "UFI: Write10"
        cmd.direct = SCS_DATA_OUT
        return cmd

    def inquiry(self):
        cmd = ScsiCmdObj()
        cmd.cdb[0] = 0x12
        cmd.cdb[4] = 0x24
        cmd.len = 0x24
        cmd.desc = "UFI: Inquiry"
        cmd.direct = SCS_DATA_IN
        return cmd

    def get_cmd_colls(self):
        cmdColl = [self.inquiry(), self.get_write_10(), self.get_read_10()]
        return cmdColl
