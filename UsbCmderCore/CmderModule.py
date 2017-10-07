



from DriverCtrl import DriverCtrl
from UsbCmderCore.CmderView import CmderView, CmderForm
from ScsiCmd import SCS_DATA_IN, SCS_DATA_OUT
from EricUtility import EricUtility
from QtUtility import QtUtility


class CmderModule:
    def execute(self, form, handleColls, rwDate):
        sel = form.cboDriverSel.currentIndex()
        handle = handleColls[sel]

        view = CmderView()
        cmd = view.get_cmdset(form)

        drvCtrl = DriverCtrl()
        drvCtrl.send_cmd(handle, cmd, rwDate)

        msg = ""
        if cmd.direct == SCS_DATA_IN:     
            util = EricUtility()
            msg = util.make_hex_table(rwDate)  
            
        return msg
        
    def get_cmd_from_form(self, form):
        cmd = 0
        view = CmderView()
        cmd = view.get_cmdset(form)
        return cmd

    def cmd_select_change(self, form, cmdColls):
        idx = form.m_cboCmdSel.currentIndex()
        cmd = cmdColls[idx]
        view = CmderView()
        view.set_form(cmd, form);

    def refresh(self, formBean):
        drv = DriverCtrl()
        drv.release_driver_list()
        driverList = drv.get_driver_list()
        if driverList[0].count != 0:
            qtUtil = QtUtility()
            qtUtil.set_qcbobox(formBean.cboDriverSel, driverList[0])

        return driverList