

from .UfiCmd import *
#from ExtenCmd import *


class ScsiCmdUtility:
    def get_cmd_colls(self):
        cmdColls = []
        ufi = UfiCmdSet()
        cmdColls.extend(ufi.get_cmd_colls())

        #extcmd = ExtendCmd()
        #cmdColls.extend(extcmd.get_cmd_colls())

        return cmdColls
    