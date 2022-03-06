# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Syllabus(object):
    def setupUi(self, Syllabus):
        Syllabus.setObjectName("Syllabus")
        Syllabus.resize(606, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Syllabus.sizePolicy().hasHeightForWidth())
        Syllabus.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Syllabus)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(Syllabus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.col_tree = QtWidgets.QTreeView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.col_tree.sizePolicy().hasHeightForWidth())
        self.col_tree.setSizePolicy(sizePolicy)
        self.col_tree.setObjectName("col_tree")
        self.verticalLayout.addWidget(self.col_tree)
        self.apply_col_settings = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apply_col_settings.sizePolicy().hasHeightForWidth())
        self.apply_col_settings.setSizePolicy(sizePolicy)
        self.apply_col_settings.setCheckable(False)
        self.apply_col_settings.setObjectName("apply_col_settings")
        self.verticalLayout.addWidget(self.apply_col_settings)
        self.export_btn = QtWidgets.QPushButton(self.groupBox)
        self.export_btn.setObjectName("export_btn")
        self.verticalLayout.addWidget(self.export_btn)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(Syllabus)
        QtCore.QMetaObject.connectSlotsByName(Syllabus)

    def retranslateUi(self, Syllabus):
        _translate = QtCore.QCoreApplication.translate
        Syllabus.setWindowTitle(_translate("Syllabus", "Syllabus"))
        self.groupBox.setTitle(_translate("Syllabus", "Co&lumn Settings"))
        self.apply_col_settings.setToolTip(_translate("Syllabus", "Apply column selections to tree"))
        self.apply_col_settings.setText(_translate("Syllabus", "Apply Columns"))
        self.export_btn.setToolTip(_translate("Syllabus", "Export current data to CSV file"))
        self.export_btn.setText(_translate("Syllabus", "Export"))
