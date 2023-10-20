# Form implementation generated from reading ui file 'PasswordManager.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1479, 874)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)
        self.lineEditNameSearch = QtWidgets.QLineEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditNameSearch.sizePolicy().hasHeightForWidth())
        self.lineEditNameSearch.setSizePolicy(sizePolicy)
        self.lineEditNameSearch.setFrame(True)
        self.lineEditNameSearch.setObjectName("lineEditNameSearch")
        self.horizontalLayout.addWidget(self.lineEditNameSearch)
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditEmailSearch = QtWidgets.QLineEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditEmailSearch.sizePolicy().hasHeightForWidth())
        self.lineEditEmailSearch.setSizePolicy(sizePolicy)
        self.lineEditEmailSearch.setObjectName("lineEditEmailSearch")
        self.horizontalLayout.addWidget(self.lineEditEmailSearch)
        self.pushButtonSearch = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonSearch.setDefault(True)
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.horizontalLayout.addWidget(self.pushButtonSearch)
        self.line = QtWidgets.QFrame(parent=self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.pushButtonClear = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.horizontalLayout.addWidget(self.pushButtonClear)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.tableWidgetLoginData = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidgetLoginData.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.tableWidgetLoginData.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.tableWidgetLoginData.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidgetLoginData.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidgetLoginData.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidgetLoginData.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableWidgetLoginData.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableWidgetLoginData.setObjectName("tableWidgetLoginData")
        self.tableWidgetLoginData.setColumnCount(0)
        self.tableWidgetLoginData.setRowCount(0)
        self.tableWidgetLoginData.horizontalHeader().setMinimumSectionSize(100)
       # self.tableWidgetLoginData.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_7.addWidget(self.tableWidgetLoginData)
        self.pushButtonExportData = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonExportData.setObjectName("pushButtonExportData")
        self.horizontalLayout_7.addWidget(self.pushButtonExportData)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButtonCancel = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        spacerItem4 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.pushButtonDelete = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.horizontalLayout_2.addWidget(self.pushButtonDelete)
        self.line_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.line_3)
        spacerItem5 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.pushButtonEdit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.horizontalLayout_2.addWidget(self.pushButtonEdit)
        self.pushButtonSave = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout_2.addWidget(self.pushButtonSave)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_newName = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_newName.setObjectName("label_newName")
        self.horizontalLayout_4.addWidget(self.label_newName)
        self.lineEditNameNewEntry = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditNameNewEntry.setObjectName("lineEditNameNewEntry")
        self.horizontalLayout_4.addWidget(self.lineEditNameNewEntry)
        self.label_newUsernameID = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_newUsernameID.setObjectName("label_newUsernameID")
        self.horizontalLayout_4.addWidget(self.label_newUsernameID)
        self.lineEditUsernameNewEntry = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditUsernameNewEntry.setObjectName("lineEditUsernameNewEntry")
        self.horizontalLayout_4.addWidget(self.lineEditUsernameNewEntry)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_newEmail = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_newEmail.setObjectName("label_newEmail")
        self.horizontalLayout_5.addWidget(self.label_newEmail)
        self.lineEditEmailNewEntry = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditEmailNewEntry.setObjectName("lineEditEmailNewEntry")
        self.horizontalLayout_5.addWidget(self.lineEditEmailNewEntry)
        self.label_newPassword = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_newPassword.setObjectName("label_newPassword")
        self.horizontalLayout_5.addWidget(self.label_newPassword)
        self.lineEditPasswordNewEntry = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditPasswordNewEntry.setObjectName("lineEditPasswordNewEntry")
        self.horizontalLayout_5.addWidget(self.lineEditPasswordNewEntry)
        self.pushButtonGenSecPass = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonGenSecPass.sizePolicy().hasHeightForWidth())
        self.pushButtonGenSecPass.setSizePolicy(sizePolicy)
        self.pushButtonGenSecPass.setMinimumSize(QtCore.QSize(160, 0))
        self.pushButtonGenSecPass.setObjectName("pushButtonGenSecPass")
        self.horizontalLayout_5.addWidget(self.pushButtonGenSecPass)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.labelPinNewEntry = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelPinNewEntry.setObjectName("labelPinNewEntry")
        self.horizontalLayout_9.addWidget(self.labelPinNewEntry)
        self.lineEditPinNewEntry = QtWidgets.QLineEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditPinNewEntry.sizePolicy().hasHeightForWidth())
        self.lineEditPinNewEntry.setSizePolicy(sizePolicy)
        self.lineEditPinNewEntry.setObjectName("lineEditPinNewEntry")
        self.horizontalLayout_9.addWidget(self.lineEditPinNewEntry)
        self.label_newNotes = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_newNotes.setObjectName("label_newNotes")
        self.horizontalLayout_9.addWidget(self.label_newNotes)
        self.lineEditNotesNewEntry = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditNotesNewEntry.setObjectName("lineEditNotesNewEntry")
        self.horizontalLayout_9.addWidget(self.lineEditNotesNewEntry)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        spacerItem8 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.pushButtonAddNewEntry = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonAddNewEntry.setMinimumSize(QtCore.QSize(200, 100))
        self.pushButtonAddNewEntry.setObjectName("pushButtonAddNewEntry")
        self.horizontalLayout_3.addWidget(self.pushButtonAddNewEntry)
        spacerItem9 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1479, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Personal Password Manager"))
        self.label_name.setText(_translate("MainWindow", "Name:"))
        self.label.setText(_translate("MainWindow", "Email:"))
        self.pushButtonSearch.setText(_translate("MainWindow", "Search"))
        self.pushButtonClear.setText(_translate("MainWindow", "Clear"))
        self.tableWidgetLoginData.setSortingEnabled(True)
        self.pushButtonExportData.setText(_translate("MainWindow", "Export Data"))
        self.pushButtonCancel.setText(_translate("MainWindow", "Cancel"))
        self.pushButtonDelete.setText(_translate("MainWindow", "Delete"))
        self.pushButtonEdit.setText(_translate("MainWindow", "Edit"))
        self.pushButtonSave.setText(_translate("MainWindow", "Save"))
        self.label_newName.setText(_translate("MainWindow", "Name:"))
        self.label_newUsernameID.setText(_translate("MainWindow", "Username/ID:"))
        self.label_newEmail.setText(_translate("MainWindow", "Email:"))
        self.label_newPassword.setText(_translate("MainWindow", "Password:"))
        self.pushButtonGenSecPass.setText(_translate("MainWindow", "Generate Secure Password"))
        self.labelPinNewEntry.setText(_translate("MainWindow", "Pin:"))
        self.label_newNotes.setText(_translate("MainWindow", "Notes:"))
        self.pushButtonAddNewEntry.setText(_translate("MainWindow", "Add New Entry"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())