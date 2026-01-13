
from PySide6.QtWidgets import (QApplication, QTextEdit, QComboBox, QCheckBox, QFileDialog)
from PySide6.QtGui import QTextCursor

import os
from EricCorePy.Utility.EricUtility import CRLF

class QtUtility:
    KEY_EVENT_PAGE_UP = 16777238
    KEY_EVENT_PAGE_DOWN = 16777239

    def __init__(self):
        self.m_last_open_dir = "."

    def set_combobox(self, cbobox: QComboBox, itemList):
        cbobox.clear()
        for item in itemList:
            cbobox.addItem(item)

    def show_alert(self, qtMsgBox, msg):
        msgBox = qtMsgBox
        msgBox.setWindowTitle('Alert')
        msgBox.setText(msg)
        msgBox.exec_()

    def is_key_event_page_down(self, event):
        return event.key() ==  self.KEY_EVENT_PAGE_DOWN

    def is_key_event_page_up(self, event):
        return event.key() ==  self.KEY_EVENT_PAGE_UP

    def to_hex_str(self, value):
        return format(value, 'X')
    
    def hex_str_to_int(self, hexStr):
        return int(hexStr, 16)  
    
    def to_hex_value(self, txtEdit: QTextEdit): 
        return self.hex_str_to_int(txtEdit.toPlainText())    
    
    def set_value_to_txtEditor(self, txtEdit: QTextEdit, number): 
        txtEdit.setText(self.to_hex_str(number)) 

    def is_check(self, ckBox: QCheckBox):
        return ckBox.isChecked()

    def upadte_ui(self):
        QApplication.processEvents() # avoid wedget hang-up issue

    def set_plain_textEditor(self, txtEditor: QTextEdit, txt: str):
        cursor = txtEditor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(txt)
        txtEditor.setTextCursor(cursor)

    def set_textEditor(self, txtEditor: QTextEdit, txt: str, isCrlf = True, isAppend = True):
        if isAppend:
            if isCrlf:
                txt = CRLF + txt
            self.set_plain_textEditor(txtEditor, txt)
        else:
            txtEditor.setPlainText(txt)
        self.upadte_ui()

    def get_file_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=None,           
            caption="select file",      
            dir=self.m_last_open_dir,              
            filter="All file (*);;Txt file(*.txt);;Python file(*.py)" 
        )

        if not file_path:
            print("cancel")

        self.m_last_open_dir = os.path.dirname(file_path)
        return file_path
  