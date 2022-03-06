# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'build/dist/designer/settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(350, 450)
        self.verticalLayout = QtWidgets.QVBoxLayout(Settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_8 = QtWidgets.QLabel(Settings)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_8)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.label = QtWidgets.QLabel(Settings)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.enablePopupDefinitions = QtWidgets.QCheckBox(Settings)
        self.enablePopupDefinitions.setObjectName("enablePopupDefinitions")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.enablePopupDefinitions)
        self.enablePopupDefinitonsOnQuestions = QtWidgets.QCheckBox(Settings)
        self.enablePopupDefinitonsOnQuestions.setEnabled(False)
        self.enablePopupDefinitonsOnQuestions.setObjectName("enablePopupDefinitonsOnQuestions")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.enablePopupDefinitonsOnQuestions)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem1)
        self.label_4 = QtWidgets.QLabel(Settings)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.label_4)
        self.label_6 = QtWidgets.QLabel(Settings)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(9, QtWidgets.QFormLayout.SpanningRole, spacerItem2)
        self.label_2 = QtWidgets.QLabel(Settings)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(Settings)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.hotkeyOpenNextPopup = QtWidgets.QKeySequenceEdit(Settings)
        self.hotkeyOpenNextPopup.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.hotkeyOpenNextPopup.setObjectName("hotkeyOpenNextPopup")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.hotkeyOpenNextPopup)
        self.label_5 = QtWidgets.QLabel(Settings)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.hotkeyOpenPreviousPopup = QtWidgets.QKeySequenceEdit(Settings)
        self.hotkeyOpenPreviousPopup.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.hotkeyOpenPreviousPopup.setObjectName("hotkeyOpenPreviousPopup")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.hotkeyOpenPreviousPopup)
        self.label_7 = QtWidgets.QLabel(Settings)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.hotkeyClosePopup = QtWidgets.QKeySequenceEdit(Settings)
        self.hotkeyClosePopup.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.hotkeyClosePopup.setObjectName("hotkeyClosePopup")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.hotkeyClosePopup)
        self.layoutColorButton = QtWidgets.QHBoxLayout()
        self.layoutColorButton.setSpacing(0)
        self.layoutColorButton.setObjectName("layoutColorButton")
        self.formLayout.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.layoutColorButton)
        self.enableArticleViewer = QtWidgets.QCheckBox(Settings)
        self.enableArticleViewer.setObjectName("enableArticleViewer")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.enableArticleViewer)
        self.label_9 = QtWidgets.QLabel(Settings)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.hotkeyToggleSidePanel = QtWidgets.QKeySequenceEdit(Settings)
        self.hotkeyToggleSidePanel.setObjectName("hotkeyToggleSidePanel")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.hotkeyToggleSidePanel)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.RestoreDefaults|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.hotkeyOpenNextPopup)
        self.label_5.setBuddy(self.hotkeyOpenPreviousPopup)
        self.label_7.setBuddy(self.hotkeyClosePopup)
        self.label_9.setBuddy(self.hotkeyToggleSidePanel)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        self.enablePopupDefinitions.toggled['bool'].connect(self.enablePopupDefinitonsOnQuestions.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Settings)
        Settings.setTabOrder(self.enablePopupDefinitions, self.enablePopupDefinitonsOnQuestions)
        Settings.setTabOrder(self.enablePopupDefinitonsOnQuestions, self.enableArticleViewer)
        Settings.setTabOrder(self.enableArticleViewer, self.hotkeyToggleSidePanel)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "AMBOSS - Settings"))
        self.label_8.setText(_translate("Settings", "AMBOSS Add-on Settings"))
        self.label.setText(_translate("Settings", "General"))
        self.enablePopupDefinitions.setToolTip(_translate("Settings", "Underline important phrases on your cards and provide hover definitions for them"))
        self.enablePopupDefinitions.setText(_translate("Settings", "&Enable pop-up definitions"))
        self.enablePopupDefinitonsOnQuestions.setToolTip(_translate("Settings", "Toggle between showing definitions on both card sides or on the answer side only"))
        self.enablePopupDefinitonsOnQuestions.setText(_translate("Settings", "Show pop-up definitions on &questions"))
        self.label_4.setText(_translate("Settings", "Styling"))
        self.label_6.setText(_translate("Settings", "Highlight color"))
        self.label_2.setText(_translate("Settings", "Keyboard Shortcuts"))
        self.label_3.setText(_translate("Settings", "Open next pop-up"))
        self.label_5.setText(_translate("Settings", "Open previous pop-up"))
        self.label_7.setText(_translate("Settings", "Close pop-up"))
        self.enableArticleViewer.setToolTip(_translate("Settings", "Whether to open AMBOSS articles within Anki or an external web browser"))
        self.enableArticleViewer.setText(_translate("Settings", "Open &articles in Anki (beta)"))
        self.label_9.setText(_translate("Settings", "Toggle side panel"))