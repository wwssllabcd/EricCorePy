from EricCore.ScsiCmd.ScsiCmdUtility import *
from EricCore.DriverCtrl import *
from EricCore.EricUtility import *
from UsbCmder.CmderView import CmderView


class CmderCtrller:
    def __init__(self, view):
        self.m_view = view
        self.m_u = EricUtility()
        cmd = ScsiCmdUtility()
        self.m_cmdset = cmd.get_cmd_colls()
        self.bind_cmd_set()

        self.m_driveSel = DriverCtrl()
        self.refresh()

    def bind_cmd_set(self):
        self.m_view.bind_cmd_set(self.m_cmdset)
        self.cmd_select_change(0)

    def refresh(self):
        self.m_driveSel.release_driver_list()
        item = self.m_driveSel.get_driver_name_list()
        self.m_view.refresh(item)

    def cmd_select_change(self, idx):
        cmd = self.m_cmdset[idx]
        self.m_view.change_select_cmd(cmd)

    def execute(self):
        curSel = self.m_view.get_cur_drive_select()
        handle = self.m_driveSel.get_driver_handle_list()[curSel]
        cmd = self.m_view.get_cmd_from_form()
        cBuf = []
        cBuf = self.m_driveSel.send_cmd(handle, cmd, cBuf)

        mainMsg = self.m_u.make_hex_table(cBuf)
        self.m_view.show_main_msg(mainMsg)

        ascii = self.m_u.make_ascii_table(cBuf)
        self.m_view.show_second_msg(ascii)
