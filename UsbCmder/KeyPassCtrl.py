from ..Utility.EricUtility import EricUtility


class KeyPassCtrl:
    def cal_cmd(self, cdb, offset, value):
        util = EricUtility()
        addr = util.get_array_value_be(cdb, offset) + value
        cdb = util.set_array_value_be(cdb, offset, addr)
        return cdb

    def adjust_lba_read(self, cmd, isPageDown):
        if cmd.cdb[0] == 0x28:
            shiltValue = -1
            if isPageDown:
                shiltValue = 1
            cmd.cdb = self.cal_cmd(cmd.cdb, 2, shiltValue)
        return cmd
    
    def page_up_down_ctrl(self, cmd, isPageDown):
        return self.adjust_lba_read(cmd, isPageDown)    
