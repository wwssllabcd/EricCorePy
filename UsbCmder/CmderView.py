
from EricCore.ScsiCmd import *
from EricCore.EricUtility import EricUtility
from EricCore.QtUtility import QtUtility

class CmderView():
    def __init__(self, ui):
        self.m_u = EricUtility()
        self.m_du = QtUtility()
        self.init_compoment(ui);
        

    def init_compoment(self, ui):
        self.m_mainMsg = ui.txtMainMsg
        self.m_cmdSel = ui.cboCmdSel
        self.m_cdb = [ui.txtCdb_00, ui.txtCdb_01, ui.txtCdb_02, ui.txtCdb_03, ui.txtCdb_04, ui.txtCdb_05,
                      ui.txtCdb_06, ui.txtCdb_07, ui.txtCdb_08, ui.txtCdb_09, ui.txtCdb_10, ui.txtCdb_11
                      ]

        self.m_dataLen = ui.txtDataLen
        self.m_dataIn = ui.rdoDataIn
        self.m_dataOut = ui.rdoDataOut
        self.m_driveSel = ui.cboDriveSel

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
