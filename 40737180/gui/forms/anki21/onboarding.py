# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/onboarding.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Onboarding(object):
    def setupUi(self, Onboarding):
        Onboarding.setObjectName("Onboarding")
        Onboarding.resize(393, 193)
        self.title = QtWidgets.QLabel(Onboarding)
        self.title.setGeometry(QtCore.QRect(0, 0, 401, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.line = QtWidgets.QFrame(Onboarding)
        self.line.setGeometry(QtCore.QRect(70, 40, 261, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.areaOfStudy = QtWidgets.QLabel(Onboarding)
        self.areaOfStudy.setGeometry(QtCore.QRect(0, 60, 401, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.areaOfStudy.setFont(font)
        self.areaOfStudy.setAlignment(QtCore.Qt.AlignCenter)
        self.areaOfStudy.setObjectName("areaOfStudy")
        self.marketId = QtWidgets.QComboBox(Onboarding)
        self.marketId.setGeometry(QtCore.QRect(100, 90, 201, 31))
        self.marketId.setObjectName("marketId")
        self.getStarted = QtWidgets.QPushButton(Onboarding)
        self.getStarted.setGeometry(QtCore.QRect(130, 150, 131, 31))
        self.getStarted.setAutoDefault(False)
        self.getStarted.setDefault(False)
        self.getStarted.setFlat(False)
        self.getStarted.setObjectName("getStarted")

        self.retranslateUi(Onboarding)
        self.getStarted.released.connect(Onboarding.accept)
        QtCore.QMetaObject.connectSlotsByName(Onboarding)

    def retranslateUi(self, Onboarding):
        _translate = QtCore.QCoreApplication.translate
        Onboarding.setWindowTitle(_translate("Onboarding", "Welcome"))
        self.title.setText(_translate("Onboarding", "Welcome to the Picmonic Anki Add-On!"))
        self.areaOfStudy.setText(_translate("Onboarding", "Please select your area of study:"))
        self.getStarted.setText(_translate("Onboarding", "Get Started"))
