# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UsbCmderUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(908, 741)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        Dialog.setFont(font)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(290, 0, 101, 101))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 81, 82))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtDataLen = QtWidgets.QLineEdit(self.layoutWidget)
        self.txtDataLen.setObjectName("txtDataLen")
        self.verticalLayout.addWidget(self.txtDataLen)
        self.rdoDataIn = QtWidgets.QRadioButton(self.layoutWidget)
        self.rdoDataIn.setObjectName("rdoDataIn")
        self.verticalLayout.addWidget(self.rdoDataIn)
        self.rdoDataOut = QtWidgets.QRadioButton(self.layoutWidget)
        self.rdoDataOut.setObjectName("rdoDataOut")
        self.verticalLayout.addWidget(self.rdoDataOut)
        self.cboCmdSel = QtWidgets.QComboBox(Dialog)
        self.cboCmdSel.setGeometry(QtCore.QRect(67, 70, 201, 25))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.cboCmdSel.setFont(font)
        self.cboCmdSel.setMaxVisibleItems(30)
        self.cboCmdSel.setObjectName("cboCmdSel")
        self.txtMainMsg = QtWidgets.QTextEdit(Dialog)
        self.txtMainMsg.setGeometry(QtCore.QRect(7, 180, 461, 541))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtMainMsg.setFont(font)
        self.txtMainMsg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txtMainMsg.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.txtMainMsg.setObjectName("txtMainMsg")
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 130, 381, 26))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtCdb_00 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_00.setObjectName("txtCdb_00")
        self.horizontalLayout.addWidget(self.txtCdb_00)
        self.txtCdb_01 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_01.setObjectName("txtCdb_01")
        self.horizontalLayout.addWidget(self.txtCdb_01)
        self.txtCdb_02 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_02.setObjectName("txtCdb_02")
        self.horizontalLayout.addWidget(self.txtCdb_02)
        self.txtCdb_03 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_03.setObjectName("txtCdb_03")
        self.horizontalLayout.addWidget(self.txtCdb_03)
        self.txtCdb_04 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_04.setObjectName("txtCdb_04")
        self.horizontalLayout.addWidget(self.txtCdb_04)
        self.txtCdb_05 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_05.setObjectName("txtCdb_05")
        self.horizontalLayout.addWidget(self.txtCdb_05)
        self.txtCdb_06 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_06.setObjectName("txtCdb_06")
        self.horizontalLayout.addWidget(self.txtCdb_06)
        self.txtCdb_07 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_07.setObjectName("txtCdb_07")
        self.horizontalLayout.addWidget(self.txtCdb_07)
        self.txtCdb_08 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_08.setObjectName("txtCdb_08")
        self.horizontalLayout.addWidget(self.txtCdb_08)
        self.txtCdb_09 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_09.setObjectName("txtCdb_09")
        self.horizontalLayout.addWidget(self.txtCdb_09)
        self.txtCdb_10 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_10.setObjectName("txtCdb_10")
        self.horizontalLayout.addWidget(self.txtCdb_10)
        self.txtCdb_11 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_11.setObjectName("txtCdb_11")
        self.horizontalLayout.addWidget(self.txtCdb_11)
        self.txtCdb_12 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_12.setObjectName("txtCdb_12")
        self.horizontalLayout.addWidget(self.txtCdb_12)
        self.txtCdb_13 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_13.setObjectName("txtCdb_13")
        self.horizontalLayout.addWidget(self.txtCdb_13)
        self.txtCdb_14 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_14.setObjectName("txtCdb_14")
        self.horizontalLayout.addWidget(self.txtCdb_14)
        self.txtCdb_15 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCdb_15.setObjectName("txtCdb_15")
        self.horizontalLayout.addWidget(self.txtCdb_15)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(7, 20, 261, 28))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cboDriveSel = QtWidgets.QComboBox(self.layoutWidget2)
        self.cboDriveSel.setObjectName("cboDriveSel")
        self.horizontalLayout_2.addWidget(self.cboDriveSel)
        self.btnExecute = QtWidgets.QPushButton(self.layoutWidget2)
        self.btnExecute.setObjectName("btnExecute")
        self.horizontalLayout_2.addWidget(self.btnExecute)
        self.btnRefresh = QtWidgets.QPushButton(self.layoutWidget2)
        self.btnRefresh.setObjectName("btnRefresh")
        self.horizontalLayout_2.addWidget(self.btnRefresh)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 160, 391, 16))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.txtAscii = QtWidgets.QTextEdit(Dialog)
        self.txtAscii.setGeometry(QtCore.QRect(480, 180, 411, 541))
        self.txtAscii.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.txtAscii.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.txtAscii.setObjectName("txtAscii")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 74, 51, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 381, 16))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "UsbCmder"))
        self.groupBox.setTitle(_translate("Dialog", "Dir"))
        self.rdoDataIn.setText(_translate("Dialog", "DataIn"))
        self.rdoDataOut.setText(_translate("Dialog", "DataOut"))
        self.btnExecute.setText(_translate("Dialog", "Execute"))
        self.btnRefresh.setText(_translate("Dialog", "Refresh"))
        self.label.setText(_translate("Dialog", "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F"))
        self.label_2.setText(_translate("Dialog", "CmdSel"))
        self.label_3.setText(_translate("Dialog", "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F"))

