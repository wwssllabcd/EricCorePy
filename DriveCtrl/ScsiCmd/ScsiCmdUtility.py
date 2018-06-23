

from .UfiCmd import *


class ScsiCmdUtility:
    def __init__(self):
        ufi = UfiCmdSet()
        self.m_ufiCmdColls = ufi.get_cmd_colls()
        self.m_extCmdColls = None

    def get_cmd_colls(self):
        cmdColls = []

        if self.m_extCmdColls != None:
            cmdColls.extend(self.m_extCmdColls)
        cmdColls.extend(self.m_ufiCmdColls)
        return cmdColls
