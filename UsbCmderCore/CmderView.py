

from ScsiCmd import ScsiCmd, UfiCmdSet
from QtUtility import QtUtility
from ScsiCmd import SCS_DATA_IN, SCS_DATA_OUT

class CmderForm:
    cboDriverSel = 0
    m_cboCmdSel = 0
    m_textCdb = []
    m_txtLength = 0
    m_rdoDataIn = 0
    m_rdoDataOut = 0

class CmderView:
    def init_cboCmdSel(self, form, cmdColls):
        for cmd in cmdColls:
             form.m_cboCmdSel.addItem(cmd.desc)

    def set_form(self, cmd, form):
        for i in range(12):
            form.m_textCdb[i].setText(format(cmd.cdb[i], '02X'))

        form.m_txtLength.setText(format(cmd.len, 'X'))
        
        if cmd.direct == SCS_DATA_IN:
            form.m_rdoDataIn.setChecked(True)
        else:
            form.m_rdoDataOut.setChecked(True)

    def get_cmdset(self, form):
        cmd = ScsiCmd()
        u = QtUtility()
        for i in range(12):
              cmd.cdb[i] = u.hex_qstr_to_int( form.m_textCdb[i].toPlainText() )

        cmd.len = u.hex_qstr_to_int(form.m_txtLength.toPlainText())

        if form.m_rdoDataIn.isChecked():
            cmd.direct = SCS_DATA_IN
        else:
            cmd.direct = SCS_DATA_OUT
        return cmd

    
