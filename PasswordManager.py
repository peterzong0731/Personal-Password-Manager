from random import SystemRandom
import sys
from PasswordManagerGUI import *
from GeneratePasswordGUI import *
import pandas as pd
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableWidget, QTableWidgetItem, QFileDialog
import os

# python -m PyQt6.uic.pyuic -x PasswordManager.ui -o PasswordManagerGUI.py

class PasswordManager():
    def __init__(self):
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.AdditionalUISetup()
        self.ConnectButtons()
        
        app.processEvents()

        self.loginData = pd.DataFrame(columns = ['Name', 'Username', 'Email', 'Password', 'Pin', 'Notes'])
        self.action = ""

        self.GetData()
        self.DisplayTable()

        sys.exit(app.exec())


    def AdditionalUISetup(self):
        pushButtonAddNewEntryFont = self.ui.pushButtonAddNewEntry.font()
        pushButtonAddNewEntryFont.setPointSize(16)
        self.ui.pushButtonAddNewEntry.setFont(pushButtonAddNewEntryFont)

        self.ui.pushButtonCancel.setVisible(False)
        self.ui.pushButtonSave.setVisible(False)



    def ConnectButtons(self):
        self.ui.pushButtonSearch.clicked.connect(self.OnFilterData)
        self.ui.pushButtonClear.clicked.connect(self.OnClearFilters)
        self.ui.pushButtonAddNewEntry.clicked.connect(self.OnAddNewEntry)
        self.ui.pushButtonEdit.clicked.connect(self.OnEdit)
        self.ui.pushButtonDelete.clicked.connect(self.OnDelete)
        self.ui.pushButtonSave.clicked.connect(self.OnSave)
        self.ui.pushButtonCancel.clicked.connect(self.OnCancel)
        self.ui.pushButtonExportData.clicked.connect(self.OnExportData)
        self.ui.pushButtonGenSecPass.clicked.connect(self.OnGeneratePassword)


    def GetData(self):
        if os.path.isfile("./Login_Data.parquet"):
            self.loginData = pd.read_parquet("./Login_Data.parquet")
        
    def SaveData(self):
        self.loginData.to_parquet("./Login_Data.parquet")

    def OnExportData(self):
        documentsFolder = os.path.join(os.environ['USERPROFILE'], 'Documents')
        defaultFileName = "MyLoginData"
        fileObj =  QFileDialog.getSaveFileName(None, 'Save File', documentsFolder + "/" + defaultFileName, "Excel (*.xlsx);;CSV (*.csv);;JSON (*.json);;XML (*.xml);;All Files (*)", "Excel (*.xlsx)")
        if fileObj[0] != '':
            fileType = os.path.splitext(fileObj[0])[1]
            match fileType:
                case ".xlsx":
                    self.loginData.to_excel(fileObj[0], index = False)
                case ".csv":
                    self.loginData.to_csv(fileObj[0], index = False)
                case ".json":
                    self.loginData.to_json(fileObj[0], index = False)
                case ".xml":
                    self.loginData.to_xml(fileObj[0], index = False)
                case _:
                    print(f"'{fileType}' is not a valid file type")
        
 

    def OnFilterData(self):
        name = self.ui.lineEditNameSearch.text().lower()
        email = self.ui.lineEditEmailSearch.text().lower()

        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            itemName = self.ui.tableWidgetLoginData.item(row, 0)
            itemEmail = self.ui.tableWidgetLoginData.item(row, 2)
            itemNameText = itemName.text().lower() if itemName else ''
            itemEmailText = itemEmail.text().lower() if itemEmail else ''

            if (name in itemNameText) and (email in itemEmailText):
                self.ui.tableWidgetLoginData.setRowHidden(row, False)
            else:
                self.ui.tableWidgetLoginData.setRowHidden(row, True)

    def OnClearFilters(self):
        print("Clearing Filters")
        self.ui.lineEditNameSearch.setText('')
        self.ui.lineEditEmailSearch.setText('')

        self.OnFilterData()


    def EnterEditDeleteUI(self):
        self.ui.pushButtonEdit.setVisible(False)
        self.ui.pushButtonDelete.setVisible(False)
        self.ui.pushButtonCancel.setVisible(True)
        self.ui.pushButtonSave.setVisible(True)
        
        self.ui.lineEditNameSearch.setDisabled(True)
        self.ui.lineEditEmailSearch.setDisabled(True)
        self.ui.pushButtonSearch.setDisabled(True)
        self.ui.pushButtonClear.setDisabled(True)
        self.ui.lineEditNameNewEntry.setDisabled(True)
        self.ui.lineEditUsernameNewEntry.setDisabled(True)
        self.ui.lineEditEmailNewEntry.setDisabled(True)
        self.ui.lineEditPasswordNewEntry.setDisabled(True)
        self.ui.pushButtonGenSecPass.setDisabled(True)
        self.ui.lineEditPinNewEntry.setDisabled(True)
        self.ui.lineEditNotesNewEntry.setDisabled(True)
        self.ui.pushButtonAddNewEntry.setDisabled(True)
        self.ui.pushButtonExportData.setDisabled(True)
        
    def ExitEditDeleteUI(self):
        self.ui.pushButtonEdit.setVisible(True)
        self.ui.pushButtonDelete.setVisible(True)
        self.ui.pushButtonCancel.setVisible(False)
        self.ui.pushButtonSave.setVisible(False)
        
        self.ui.lineEditNameSearch.setEnabled(True)
        self.ui.lineEditEmailSearch.setEnabled(True)
        self.ui.pushButtonSearch.setEnabled(True)
        self.ui.pushButtonClear.setEnabled(True)
        self.ui.lineEditNameNewEntry.setEnabled(True)
        self.ui.lineEditUsernameNewEntry.setEnabled(True)
        self.ui.lineEditEmailNewEntry.setEnabled(True)
        self.ui.lineEditPasswordNewEntry.setEnabled(True)
        self.ui.pushButtonGenSecPass.setEnabled(True)
        self.ui.lineEditPinNewEntry.setEnabled(True)
        self.ui.lineEditNotesNewEntry.setEnabled(True)
        self.ui.pushButtonAddNewEntry.setEnabled(True)
        self.ui.pushButtonExportData.setEnabled(True)
        
        self.ui.tableWidgetLoginData.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.ui.tableWidgetLoginData.clearSelection()


    def OnEdit(self):
        self.EnterEditDeleteUI()
        self.ui.tableWidgetLoginData.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.action = "Edit"

    def OnSave(self):
        print("Saving changes")
        self.ExitEditDeleteUI()

        if self.action == "Edit":
            self.ApplyEdits()
        elif self.action == "Delete":
            self.DeleteRows()

        self.action = ""

    def OnCancel(self):
        print("Cancel changes")
        self.ExitEditDeleteUI()

        if self.action == "Edit":
            self.DisplayTable()

        self.action = ""

    def OnDelete(self):
        self.EnterEditDeleteUI()
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.action = "Delete"
        

    
    def OnAddNewEntry(self):
        # Perform checks that the necessary fields are filled in
        
        newEntryData = {
                        'Name': [self.ui.lineEditNameNewEntry.text()],
                        'Username': [self.ui.lineEditUsernameNewEntry.text()],
                        'Email': [self.ui.lineEditEmailNewEntry.text()],
                        'Password': [self.ui.lineEditPasswordNewEntry.text()],
                        'Pin': [self.ui.lineEditPinNewEntry.text()],
                        'Notes': [self.ui.lineEditNotesNewEntry.text()]
                       }
        
        if newEntryData['Name'][0].strip() == '':
            print("Name can't be empty")
            return

        newEntryDF = pd.DataFrame(newEntryData)
        
        self.loginData = pd.concat([self.loginData, newEntryDF], ignore_index = True)

        self.DisplayTable()
        self.SaveData()


    def LastColumnFits(self):
        total_width = self.ui.tableWidgetLoginData.viewport().width()
        column_width_sum = 0

        for column in range(self.ui.tableWidgetLoginData.columnCount()):
            column_width_sum += self.ui.tableWidgetLoginData.horizontalHeader().sectionSize(column)

        return total_width >= column_width_sum
    
    def DisplayTable(self):
        self.ui.tableWidgetLoginData.setRowCount(self.loginData.shape[0])
        self.ui.tableWidgetLoginData.setColumnCount(self.loginData.shape[1])
        self.ui.tableWidgetLoginData.setHorizontalHeaderLabels(self.loginData.columns)        

        dataList = self.loginData.values.tolist()
        for row in range(len(dataList)):
            for col in range(len(dataList[0])):
                self.ui.tableWidgetLoginData.setItem(row, col, QTableWidgetItem(str(dataList[row][col])))

        self.ui.tableWidgetLoginData.repaint()

        self.ui.tableWidgetLoginData.resizeColumnsToContents()
        
        if self.LastColumnFits():
            self.ui.tableWidgetLoginData.horizontalHeader().setSectionResizeMode(self.ui.tableWidgetLoginData.columnCount() - 1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.tableWidgetLoginData.horizontalHeader().setStretchLastSection(True)


    def ApplyEdits(self):       
        numRows = self.ui.tableWidgetLoginData.rowCount()
        numColumns = self.ui.tableWidgetLoginData.columnCount()

        updatedData = []

        for row in range(numRows):
            row_data = []
            for col in range(numColumns):
                item = self.ui.tableWidgetLoginData.item(row, col)
                if item:
                    row_data.append(item.text())
            updatedData.append(row_data)

        self.loginData = pd.DataFrame(updatedData, columns = ['Name', 'Username', 'Email', 'Password', 'Pin', 'Notes'])

        self.SaveData()
        self.DisplayTable()


    def DeleteRows(self):
        print("Deleting")

        selectedRows = []
        for item in self.ui.tableWidgetLoginData.selectedItems():
            selectedRows.append(item.row())
        selectedRows = sorted(selectedRows, reverse = True)

        self.loginData = self.loginData.drop(index = selectedRows)

        self.ui.tableWidgetLoginData.clearSelection()

        for row in selectedRows:
            self.ui.tableWidgetLoginData.removeRow(row)



    def OnGeneratePassword(self):
        PasswordObj = PasswordGenerator()
        self.ui.lineEditPasswordNewEntry.setText(PasswordObj.GetPassword())



class PasswordGenerator():
    def __init__(self):
        # All possible characters in a password
        self.lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.specialSymbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', '[', ']', '{', '}', '<', '>']

        # Cryptographically secure randomizer
        self.sys_random = SystemRandom()

        # Create Password Generator Dialog
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()

        self.Dialog.exec()


    def AdditionalUISetup(self):
        labelOptionsFont = self.ui.labelPwdOptions.font()
        labelOptionsFont.setPointSize(16)
        self.ui.labelPwdOptions.setFont(labelOptionsFont)

        self.ui.labelPwdCopiedtoClipboard.setVisible(False)


    def ConnectButtons(self):
        self.ui.pushButtonPwdGeneratePwd.clicked.connect(self.GeneratePassword)
        self.ui.pushButtonPwdCancel.clicked.connect(self.OnCancel)
        self.ui.pushButtonPwdOK.clicked.connect(self.CloseDialog)


    def GeneratePassword(self):
        password = []
        length = self.ui.spinBoxPwdLen.value()

        # Passwords must be at least 4 characters long
        if length < 4:
            print("Error")
            return -1

        remainingChars = length

        # If the password will contain numbers
        if self.ui.checkBoxPwdIncludeNumbers.isChecked():
            numNumbers = self.sys_random.randint(1, length // 2.5)
            # If the password will contain numbers and symbols
            if self.ui.checkBoxPwdIncludeSymbols.isChecked():
                numSymbols = min(self.sys_random.randint(1, length // 2.5), length - 3)
                remainingChars -= numSymbols
                randSymbols = self.sys_random.choices(self.specialSymbols, k = numSymbols)
                password = randSymbols

                numNumbers = min(numNumbers, remainingChars - 2)


            remainingChars -= numNumbers
            password += self.sys_random.choices(self.numbers, k = numNumbers)
            
            numUppercase = self.sys_random.randint(1, remainingChars - 1)
            remainingChars -= numUppercase

        # If the password will contain symbols but not numbers
        elif self.ui.checkBoxPwdIncludeSymbols.isChecked():
            numSymbols = min(self.sys_random.randint(1, length // 2.5), length - 2)
            remainingChars -= numSymbols
            randSymbols = self.sys_random.choices(self.specialSymbols, k = numSymbols)
            password = randSymbols

            numUppercase = self.sys_random.randint(1, remainingChars - 1)
            remainingChars -= numUppercase

        # If the password will only contain letters
        else:
            numUppercase = self.sys_random.randint(1, length - 1)
            remainingChars -= numUppercase

        # Choose uppercase letters
        password += self.sys_random.choices(self.uppercaseLetters, k = numUppercase)
        # Choose lowercase letters
        password += self.sys_random.choices(self.lowercaseLetters, k = remainingChars)

        # Shuffle the password order. Doesn't make it any more random
        self.sys_random.shuffle(password)

        # If there is a length mismatch, which should not happen
        if (len(password) != length):
            print ("Error length mismatch: " + str(len(password)) + " v.s. " + str(length))

        # Save the password as a string
        self.ui.lineEditPwdPassword.setText(''.join(password))

        # Copy password to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.lineEditPwdPassword.text())
        self.ui.labelPwdCopiedtoClipboard.setVisible(True)
        self.ui.lineEditPwdPassword.selectAll()

    def GetPassword(self):
        return self.ui.lineEditPwdPassword.text()
    

    def CloseDialog(self):
        self.Dialog.close()

    def OnCancel(self):
        self.ui.lineEditPwdPassword.setText("")
        self.CloseDialog()
    



if __name__ == "__main__":
    passMngr = PasswordManager()
