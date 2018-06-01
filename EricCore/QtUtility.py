

class QtUtility:
    def set_combobox(self, cbobox, itemList):
        cbobox.clear()
        for item in itemList:
            cbobox.addItem(item)

    def show_alert(self, QtGui, msg):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle('Alert')
        msgBox.setText(msg)
        msgBox.exec_()


    def is_rdo_check(self, rdoBtn):
        return rdoBtn.isChecked()
