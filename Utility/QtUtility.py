
class QtUtility:
    KEY_EVENT_PAGE_UP = 16777238
    KEY_EVENT_PAGE_DOWN = 16777239

    def set_combobox(self, cbobox, itemList):
        cbobox.clear()
        for item in itemList:
            cbobox.addItem(item)

    def show_alert(self, qtMsgBox, msg):
        msgBox = qtMsgBox
        msgBox.setWindowTitle('Alert')
        msgBox.setText(msg)
        msgBox.exec_()

    def is_rdo_check(self, rdoBtn):
        return rdoBtn.isChecked()

    def is_key_event_page_down(self, event):
        return event.key() ==  self.KEY_EVENT_PAGE_DOWN

    def is_key_event_page_up(self, event):
        return event.key() ==  self.KEY_EVENT_PAGE_UP
            
        

