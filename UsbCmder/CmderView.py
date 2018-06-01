
from EricCorePy.ScsiUtility.ScsiCmd.ScsiCmdUtility import *
from EricCorePy.Utility.EricUtility import EricUtility
from EricCorePy.QtUtility.QtUtility import QtUtility


class CmderView():
    def __init__(self):
        self.m_u = EricUtility()
        self.m_du = QtUtility()

        self.m_mainMsg = None
        self.m_secondMsg = None
        self.m_cmdSel = None
        self.m_cdb = []

        self.m_dataLen = None
        self.m_dataIn = None
        self.m_dataOut = None
        self.m_driveSel = None

    def refresh(self, item):
        self.m_du.set_combobox(self.m_driveSel, item)

    def bind_cmd_set(self, cmdSet):
        item = []
        for c in cmdSet:
            item.append(c.desc)
        self.m_du.set_combobox(self.m_cmdSel, item)

    def change_select_cmd(self, cmd):
        for i in range(12):
            s = self.m_u.to_hex_string(cmd.cdb[i])
            self.m_cdb[i].setText(s)
        self.m_dataLen.setText(self.m_u.to_hex_string(cmd.len))

        if cmd.direct == SCS_DATA_IN:
            self.m_dataIn.setChecked(True)
        else:
            self.m_dataOut.setChecked(True)

    def get_cur_drive_select(self):
        return self.m_driveSel.currentIndex()

    def show_main_msg(self, msg):
        if self.m_mainMsg != None:
            self.m_mainMsg.setText(msg)
        else:
            print("main msg is None")

    def show_second_msg(self, msg):
        if self.m_secondMsg != None:
            self.m_secondMsg.setText(msg)
        else:
            print("second msg is None")
                

    def is_dataIn_check(self):
        if self.m_du.is_rdo_check(self.m_dataIn):
            return True
        return False

    def get_cmd_from_form(self):
        cmd = ScsiCmdObj()
        for i in range(12):
            cmd.cdb[i] = self.m_u.hex_string_to_int(self.m_cdb[i].text())

        cmd.len = self.m_u.hex_string_to_int(self.m_dataLen.text())

        if self.is_dataIn_check():
            cmd.direct = SCS_DATA_IN
        else:
            cmd.direct = SCS_DATA_OUT

        return cmd
