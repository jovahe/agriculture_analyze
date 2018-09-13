# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MoreOne.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(444, 208)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 90, 431, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setEnabled(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_two = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_two.setEnabled(True)
        self.lineEdit_two.setObjectName("lineEdit_two")
        self.horizontalLayout_2.addWidget(self.lineEdit_two)
        self.pushButton_two = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_two.setEnabled(True)
        self.pushButton_two.setObjectName("pushButton_two")
        self.horizontalLayout_2.addWidget(self.pushButton_two)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 30, 431, 41))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_one = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_one.setEnabled(True)
        self.lineEdit_one.setObjectName("lineEdit_one")
        self.horizontalLayout.addWidget(self.lineEdit_one)
        self.pushButton_one = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_one.setEnabled(True)
        self.pushButton_one.setObjectName("pushButton_one")
        self.horizontalLayout.addWidget(self.pushButton_one)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(250, 160, 177, 29))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_cancel = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_3.addWidget(self.pushButton_cancel)
        self.pushButton_ok = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_3.addWidget(self.pushButton_ok)

        self.retranslateUi(Dialog)
        self.pushButton_one.clicked.connect(Dialog.sopen1)
        self.pushButton_two.clicked.connect(Dialog.sopen2)
        self.pushButton_ok.clicked.connect(Dialog.sok)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "File_two"))
        self.pushButton_two.setText(_translate("Dialog", "Open"))
        self.label.setText(_translate("Dialog", "File_one"))
        self.pushButton_one.setText(_translate("Dialog", "Open"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))
        self.pushButton_ok.setText(_translate("Dialog", "Ok"))

