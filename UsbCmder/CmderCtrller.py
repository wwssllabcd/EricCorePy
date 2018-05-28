from EricCore.ScsiCmd import *
from EricCore.DriverCtrl import *


class CmderCtrller:
    def __init__(self, view):
        self.m_view = view
        cmd = UfiCmdSet()
        self.m_cmdset = cmd.get_cmd_colls()
        self.bind_cmd_set()

        self.m_driveSel = DriverCtrl()
        self.refresh()

    def bind_cmd_set(self):
        self.m_view.bind_cmd_set(self.m_cmdset)
        self.cmd_select_change(0)

    def refresh(self):
        item = self.m_driveSel.get_driver_list()
        print(item)
        strDrv = ["test1", "test2"]
        self.m_view.refresh(strDrv)

    def cmd_select_change(self, idx):
        cmd = self.m_cmdset[idx]
        self.m_view.change_select_cmd(cmd)
