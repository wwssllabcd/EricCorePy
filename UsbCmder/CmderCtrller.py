from ..DriveCtrl.ScsiCmd.ScsiCmdUtility import ScsiCmdUtility
from ..DriveCtrl.DriverCtrl import DriverCtrl
from ..Utility.EricUtility import EricUtility
from ..Utility.QtUtility import QtUtility

from ..UsbCmder.CmderView import CmderView
from ..UsbCmder.KeyPassCtrl import KeyPassCtrl

class CmderCtrller:
    def __init__(self, view):
        self.m_view = view
        self.m_u = EricUtility()
        self.m_driveSel = DriverCtrl()
        self.m_keyPassCtrl = KeyPassCtrl()
        self.m_qtu = QtUtility()

        self.m_keyPassCtrlExt = None
        self.m_dataParser = None
        self.m_extCmdColls = None

        self.refresh()

    def bind_cmd_set(self):
        cmd = ScsiCmdUtility()
        cmdColls = cmd.get_cmd_colls()

        if self.m_extCmdColls != None:
            self.m_extCmdColls.extend(cmdColls)
            cmdColls = self.m_extCmdColls

        self.m_cmdset = cmdColls
        self.m_view.bind_cmd_set(self.m_cmdset)
        self.cmd_select_change(0)

    def refresh(self):
        self.m_driveSel.release_driver_list()
        item = self.m_driveSel.get_driver_name_list()
        self.m_view.refresh(item)

    def cmd_select_change(self, idx):
        cmd = self.m_cmdset[idx]
        self.m_view.change_select_cmd(cmd)
        
    def key_press_event_ext(self, cmd, isPageDown):
        if self.m_keyPassCtrlExt != None:
            cmd = self.m_keyPassCtrlExt.page_up_down_ctrl(cmd, isPageDown)
        return cmd
        
    def key_press_event(self, event):
        if self.m_qtu.is_key_event_page_up(event) or self.m_qtu.is_key_event_page_down(event):
            isPageDown = self.m_qtu.is_key_event_page_down(event)
            cmd = self.m_view.get_cmd_from_form()
            cmd = self.m_keyPassCtrl.page_up_down_ctrl(cmd, isPageDown)
            cmd = self.key_press_event_ext(cmd, isPageDown)
            self.m_view.change_select_cmd(cmd)
            self.execute()
            return True
        return False

    def execute(self):
        try:
            curSel = self.m_view.get_cur_drive_select()
            handle = self.m_driveSel.get_driver_handle_list()[curSel]
            cmd = self.m_view.get_cmd_from_form()
            cBuf = []
            cBuf = self.m_driveSel.send_cmd(handle, cmd, cBuf)

            mainMsg = self.m_u.make_hex_table(cBuf)
            self.m_view.show_main_msg(mainMsg)

            #secondMsg = ""
            secondMsg = self.m_u.make_ascii_table(cBuf)
            if len(cBuf) != 0:
                secondMsg = "ASCII\r\n" + secondMsg

            if self.m_dataParser != None:
                secondMsg = self.m_dataParser.parser(cmd, cBuf) + secondMsg
            self.m_view.show_second_msg(secondMsg)
        except:
            self.m_view.show_alert("error")
