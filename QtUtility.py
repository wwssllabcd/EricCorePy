

class QtUtility:
    def set_qcbobox(self, qcbobox, itemList):
        qcbobox.clear()
        for item in itemList:
            qcbobox.addItem(item)

    def hex_qstr_to_int(self, hexQStr):
        return int(str(hexQStr), 16)

    def show_alert(self, QtGui, msg):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle('Alert')
        msgBox.setText(msg)
        msgBox.exec_()
