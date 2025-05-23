# Form implementation generated from reading ui file 'ManagePreferences.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogManagePreferences(object):
    def setupUi(self, DialogManagePreferences):
        DialogManagePreferences.setObjectName("DialogManagePreferences")
        DialogManagePreferences.resize(403, 483)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogManagePreferences)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelPreferences = QtWidgets.QLabel(parent=DialogManagePreferences)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        font.setUnderline(True)
        self.labelPreferences.setFont(font)
        self.labelPreferences.setObjectName("labelPreferences")
        self.verticalLayout.addWidget(self.labelPreferences)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea = QtWidgets.QScrollArea(parent=DialogManagePreferences)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 358, 425))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayoutTheme = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTheme.setObjectName("horizontalLayoutTheme")
        self.labelTheme = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.labelTheme.setFont(font)
        self.labelTheme.setObjectName("labelTheme")
        self.horizontalLayoutTheme.addWidget(self.labelTheme)
        self.comboBoxTheme = QtWidgets.QComboBox(parent=self.scrollAreaWidgetContents)
        self.comboBoxTheme.setObjectName("comboBoxTheme")
        self.horizontalLayoutTheme.addWidget(self.comboBoxTheme)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutTheme.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayoutTheme)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayoutHidePasswords = QtWidgets.QHBoxLayout()
        self.horizontalLayoutHidePasswords.setObjectName("horizontalLayoutHidePasswords")
        self.checkBoxHidePasswordsByDefault = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxHidePasswordsByDefault.sizePolicy().hasHeightForWidth())
        self.checkBoxHidePasswordsByDefault.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.checkBoxHidePasswordsByDefault.setFont(font)
        self.checkBoxHidePasswordsByDefault.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkBoxHidePasswordsByDefault.setStyleSheet("QCheckBox {padding-left: 0px;}")
        self.checkBoxHidePasswordsByDefault.setObjectName("checkBoxHidePasswordsByDefault")
        self.horizontalLayoutHidePasswords.addWidget(self.checkBoxHidePasswordsByDefault)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutHidePasswords.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayoutHidePasswords)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayoutTableHeaderRowColor = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTableHeaderRowColor.setObjectName("horizontalLayoutTableHeaderRowColor")
        self.labelTableHeaderRowColor = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.labelTableHeaderRowColor.setFont(font)
        self.labelTableHeaderRowColor.setObjectName("labelTableHeaderRowColor")
        self.horizontalLayoutTableHeaderRowColor.addWidget(self.labelTableHeaderRowColor)
        self.verticalLayout_2.addLayout(self.horizontalLayoutTableHeaderRowColor)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayoutTableNameColumnColor = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTableNameColumnColor.setObjectName("horizontalLayoutTableNameColumnColor")
        self.labelTableNameColumnColor = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.labelTableNameColumnColor.setFont(font)
        self.labelTableNameColumnColor.setObjectName("labelTableNameColumnColor")
        self.horizontalLayoutTableNameColumnColor.addWidget(self.labelTableNameColumnColor)
        self.verticalLayout_2.addLayout(self.horizontalLayoutTableNameColumnColor)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayoutCategoryColor = QtWidgets.QHBoxLayout()
        self.horizontalLayoutCategoryColor.setObjectName("horizontalLayoutCategoryColor")
        self.labelDefaultCategoryColor = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.labelDefaultCategoryColor.setFont(font)
        self.labelDefaultCategoryColor.setObjectName("labelDefaultCategoryColor")
        self.horizontalLayoutCategoryColor.addWidget(self.labelDefaultCategoryColor)
        self.verticalLayout_2.addLayout(self.horizontalLayoutCategoryColor)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem7)
        self.labelDefaultPasswordOptions = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.labelDefaultPasswordOptions.setFont(font)
        self.labelDefaultPasswordOptions.setObjectName("labelDefaultPasswordOptions")
        self.verticalLayout_2.addWidget(self.labelDefaultPasswordOptions)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelLength = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelLength.setFont(font)
        self.labelLength.setObjectName("labelLength")
        self.horizontalLayout_3.addWidget(self.labelLength)
        self.spinBoxDefaultPasswordLength = QtWidgets.QSpinBox(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDefaultPasswordLength.sizePolicy().hasHeightForWidth())
        self.spinBoxDefaultPasswordLength.setSizePolicy(sizePolicy)
        self.spinBoxDefaultPasswordLength.setMinimumSize(QtCore.QSize(50, 0))
        self.spinBoxDefaultPasswordLength.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxDefaultPasswordLength.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.spinBoxDefaultPasswordLength.setMinimum(4)
        self.spinBoxDefaultPasswordLength.setMaximum(50)
        self.spinBoxDefaultPasswordLength.setObjectName("spinBoxDefaultPasswordLength")
        self.horizontalLayout_3.addWidget(self.spinBoxDefaultPasswordLength)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBoxDefaultPasswordIncludeNumbers = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.checkBoxDefaultPasswordIncludeNumbers.setFont(font)
        self.checkBoxDefaultPasswordIncludeNumbers.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkBoxDefaultPasswordIncludeNumbers.setStyleSheet("QCheckBox {padding-left: 0px;}")
        self.checkBoxDefaultPasswordIncludeNumbers.setObjectName("checkBoxDefaultPasswordIncludeNumbers")
        self.horizontalLayout_4.addWidget(self.checkBoxDefaultPasswordIncludeNumbers)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBoxDefaultPasswordIncludeSymbols = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.checkBoxDefaultPasswordIncludeSymbols.setFont(font)
        self.checkBoxDefaultPasswordIncludeSymbols.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkBoxDefaultPasswordIncludeSymbols.setStyleSheet("QCheckBox {padding-left: 0px;}")
        self.checkBoxDefaultPasswordIncludeSymbols.setObjectName("checkBoxDefaultPasswordIncludeSymbols")
        self.horizontalLayout_5.addWidget(self.checkBoxDefaultPasswordIncludeSymbols)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem12)
        self.pushButtonCancel = QtWidgets.QPushButton(parent=DialogManagePreferences)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(parent=DialogManagePreferences)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogManagePreferences)
        QtCore.QMetaObject.connectSlotsByName(DialogManagePreferences)

    def retranslateUi(self, DialogManagePreferences):
        _translate = QtCore.QCoreApplication.translate
        DialogManagePreferences.setWindowTitle(_translate("DialogManagePreferences", "Dialog"))
        self.labelPreferences.setText(_translate("DialogManagePreferences", "Preferences"))
        self.labelTheme.setText(_translate("DialogManagePreferences", "Theme:"))
        self.checkBoxHidePasswordsByDefault.setText(_translate("DialogManagePreferences", "Hide Passwords By Default:"))
        self.labelTableHeaderRowColor.setText(_translate("DialogManagePreferences", "Table Header Row Color:"))
        self.labelTableNameColumnColor.setText(_translate("DialogManagePreferences", "Table Name Column Color:"))
        self.labelDefaultCategoryColor.setText(_translate("DialogManagePreferences", "Default Category Color:"))
        self.labelDefaultPasswordOptions.setText(_translate("DialogManagePreferences", "Default Password Options:"))
        self.labelLength.setText(_translate("DialogManagePreferences", "Length:"))
        self.checkBoxDefaultPasswordIncludeNumbers.setText(_translate("DialogManagePreferences", "Include Numbers:"))
        self.checkBoxDefaultPasswordIncludeSymbols.setText(_translate("DialogManagePreferences", "Include Symbols:"))
        self.pushButtonCancel.setText(_translate("DialogManagePreferences", "Cancel"))
        self.pushButtonApply.setText(_translate("DialogManagePreferences", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogManagePreferences = QtWidgets.QDialog()
    ui = Ui_DialogManagePreferences()
    ui.setupUi(DialogManagePreferences)
    DialogManagePreferences.show()
    sys.exit(app.exec())
