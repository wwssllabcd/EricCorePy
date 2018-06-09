
SCS_DATA_IN = 0x02
SCS_DATA_OUT = 0x04
SCS_DATA_NON = 0x02


class ScsiCmdObj:
    def __init__(self):
        self.cdb = [0]*16
        self.len = 0
        self.desc = ""
        self.direct = SCS_DATA_OUT
