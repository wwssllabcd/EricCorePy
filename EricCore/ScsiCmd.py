SCS_DATA_IN = 0x02
SCS_DATA_OUT = 0x04
SCS_DATA_NON = 0x02


class ScsiCmd:
    def __init__(self):
        self.cdb = [0]*12
        self.len = 0
        self.desc = ""
        self.direct = SCS_DATA_OUT


class UfiCmdSet:
    def _get_read_10(self):
        cmd = ScsiCmd()
        cmd.cdb[0] = 0x28
        cmd.cdb[8] = 0x01
        cmd.len = cmd.cdb[8]*512
        cmd.direct = SCS_DATA_IN
        cmd.desc = "UFI: Read10"
        return cmd

    def _get_write_10(self):
        cmd = ScsiCmd()
        cmd.cdb[0] = 0x2A
        cmd.cdb[8] = 0x01
        cmd.len = cmd.cdb[8]*512
        cmd.desc = "UFI: Write10"
        cmd.direct = SCS_DATA_OUT
        return cmd

    def _inquiry(self):
        cmd = ScsiCmd()
        cmd.cdb[0] = 0x12
        cmd.cdb[4] = 0x24
        cmd.len = 0x24
        cmd.desc = "UFI: Inquiry"
        cmd.direct = SCS_DATA_IN
        return cmd

    def get_cmd_colls(self):
        cmdColl = [self._inquiry(), self._get_write_10(), self._get_read_10()]
        return cmdColl
