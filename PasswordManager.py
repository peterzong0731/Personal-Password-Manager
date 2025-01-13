from random import SystemRandom
import sys
from PasswordManagerGUI import *
import GeneratePasswordGUI
import ImportFileOptionsGUI
import pandas as pd
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableWidget, QTableWidgetItem, QFileDialog, QStatusBar
from PyQt6.QtCore import pyqtSignal
import os

# python -m PyQt6.uic.pyuic -x PasswordManager.ui -o PasswordManagerGUICopy.py

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

        self.expectedColumns = ['Name', 'Username', 'Email', 'Password', 'Pin', 'Notes']
        self.loginData = pd.DataFrame(columns = self.expectedColumns)

        self.GetData()
        self.DisplayTable()

        sys.exit(app.exec())


    def AdditionalUISetup(self):
        pushButtonAddNewEntryFont = self.ui.pushButtonAddNewEntry.font()
        pushButtonAddNewEntryFont.setPointSize(16)
        self.ui.pushButtonAddNewEntry.setFont(pushButtonAddNewEntryFont)

        self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditUsernameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditEmailNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditPasswordNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditPinNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditNotesNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        
        self.ui.lineEditNameNewEntry.textChanged.connect(
            lambda: (
                self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}"),
                self.ClearStatusBar()
            )
        )

        self.ui.pushButtonCancel.setVisible(False)
        self.ui.pushButtonConfirm.setVisible(False)

        self.ui.lineEditNameSearch.textChanged.connect(self.OnFilterData)
        self.ui.lineEditEmailSearch.textChanged.connect(self.OnFilterData)

        self.status_bar = QStatusBar()
        self.MainWindow.setStatusBar(self.status_bar)


    def ConnectButtons(self):
        self.ui.pushButtonAddNewEntry.clicked.connect(self.OnAddNewEntry)
        self.ui.pushButtonEdit.clicked.connect(self.OnEdit)
        self.ui.pushButtonDelete.clicked.connect(self.OnDelete)
        self.ui.pushButtonConfirm.clicked.connect(self.OnConfirm)
        self.ui.pushButtonCancel.clicked.connect(self.OnCancel)
        self.ui.pushButtonImportData.clicked.connect(self.OnImportData)
        self.ui.pushButtonExportData.clicked.connect(self.OnExportData)
        self.ui.pushButtonGenSecPass.clicked.connect(self.OnGeneratePassword)
        self.ui.pushButtonRemoveDuplicates.clicked.connect(self.OnRemoveDuplicates)


    def GetData(self):
        if os.path.isfile("./Login_Data.parquet"):
            self.loginData = pd.read_parquet("./Login_Data.parquet")
        
    def SaveData(self):
        self.loginData.to_parquet("./Login_Data.parquet")


    def OnImportData(self):
        self.ClearStatusBar()
        fileObj = QFileDialog.getOpenFileName(None, "Open File", "", "Excel (*.xlsx);;CSV (*.csv);;JSON (*.json);;XML (*.xml);;Parquet (*.parquet);;All Files (*)")
        if fileObj[0] == "":
            return
        
        self.importedData = None
        fileType = os.path.splitext(fileObj[0])[1]
        match fileType:
            case ".xlsx":
                self.importedData = pd.read_excel(fileObj[0], dtype=str)
            case ".csv":
                self.importedData = pd.read_csv(fileObj[0], dtype=str)
            case ".json":
                self.importedData = pd.read_json(fileObj[0], dtype=str)
            case ".xml":
                self.importedData = pd.read_xml(fileObj[0], dtype=str)
            case ".parquet":
                self.importedData = pd.read_parquet(fileObj[0])
            case _:
                self.UpdateStatusBar(f"Invalid file selected, '{fileType}' is not a valid file type", "red")
                return
            
        # Check if the columns match up
        if set(self.expectedColumns) != set(self.importedData.columns):
            missingColumns = set(self.expectedColumns) - set(self.importedData.columns)
            extraColumns = set(self.importedData.columns) - set(self.expectedColumns)
            statusBarMessage = "Error importing data."
            if len(missingColumns) > 0:
                statusBarMessage += " Missing columns: [" + ", ".join(missingColumns) + "]."
            if len(extraColumns) > 0:
                statusBarMessage += " Unexpected columns: [" + ", ".join(missingColumns) + "]."
            self.UpdateStatusBar(statusBarMessage, "red")
            return
                
        self.importedData = self.importedData.fillna("")

        importFileObj = ImportFileOptions()
        importFileObj.dialogClosed.connect(self.OnImportFileDialogClosed)
        importFileObj.Dialog.exec()

    def OnImportFileDialogClosed(self, response):
        if response == "Cancel":
            return
        elif response == "Add":
            self.loginData = pd.concat([self.loginData, self.importedData])
            self.loginData = self.loginData.drop_duplicates()
            self.UpdateStatusBar('Data imported with the "Add" mode')
        elif response == "Replace":
            self.loginData = self.importedData
            self.UpdateStatusBar('Data imported with the "Replace" mode')

        self.DisplayTable()
        self.SaveData()

    def OnExportData(self):
        self.ClearStatusBar()
        defaultFileName = "LoginData.xlsx"
        fileObj =  QFileDialog.getSaveFileName(None, "Save File", defaultFileName, "Excel (*.xlsx);;CSV (*.csv);;JSON (*.json);;XML (*.xml);;Parquet (*.parquet);;All Files (*)")
        if fileObj[0] == "":
            return
        
        # Check if file is in currently in use/open
        if os.path.exists(fileObj[0]):
            try:
                fd = os.open(fileObj[0], os.O_RDWR | os.O_EXCL)
                os.close(fd)
            except OSError as e:
                print(e)
                self.UpdateStatusBar("Failed to export file because it is currently in use. Please close it and try again.", "red")
                return

        fileType = os.path.splitext(fileObj[0])[1]
        match fileType:
            case ".xlsx":
                self.loginData.to_excel(fileObj[0], index = False)
                self.UpdateStatusBar(".xlsx file exported")
            case ".csv":
                self.loginData.to_csv(fileObj[0], index = False)
                self.UpdateStatusBar(".csv file exported")
            case ".json":
                self.loginData.to_json(fileObj[0], index = False)
                self.UpdateStatusBar(".json file exported")
            case ".xml":
                self.loginData.to_xml(fileObj[0], index = False)
                self.UpdateStatusBar(".xml file exported")
            case ".parquet":
                self.loginData.to_parquet(fileObj[0], index = False)
                self.UpdateStatusBar(".parquet file exported")
            case _:
                self.UpdateStatusBar(f"Invalid file selected, '{fileType}' is not a valid file type", "red")


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


    def OnRemoveDuplicates(self):
        oldDataFrame = self.loginData
        self.loginData = oldDataFrame.drop_duplicates()

        duplicatesDropped = oldDataFrame.shape[0] - self.loginData.shape[0]
        if duplicatesDropped == 0:
            self.UpdateStatusBar("No duplicates found")
        elif duplicatesDropped == 1:
            self.UpdateStatusBar("1 duplicate removed")
        else:
            self.UpdateStatusBar(str(duplicatesDropped) + " duplicates removed")

        self.DisplayTable()
        self.SaveData()


    def EnterEditDeleteUI(self):
        self.ui.pushButtonEdit.setVisible(False)
        self.ui.pushButtonDelete.setVisible(False)
        self.ui.pushButtonCancel.setVisible(True)
        self.ui.pushButtonConfirm.setVisible(True)
        
        self.ui.lineEditNameSearch.setDisabled(True)
        self.ui.lineEditEmailSearch.setDisabled(True)
        self.ui.lineEditNameNewEntry.setDisabled(True)
        self.ui.lineEditUsernameNewEntry.setDisabled(True)
        self.ui.lineEditEmailNewEntry.setDisabled(True)
        self.ui.lineEditPasswordNewEntry.setDisabled(True)
        self.ui.pushButtonGenSecPass.setDisabled(True)
        self.ui.lineEditPinNewEntry.setDisabled(True)
        self.ui.lineEditNotesNewEntry.setDisabled(True)
        self.ui.pushButtonAddNewEntry.setDisabled(True)
        self.ui.pushButtonExportData.setDisabled(True)

        self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {color: gray, border: 1px solid gray;}")
        self.ui.lineEditUsernameNewEntry.setStyleSheet("QLineEdit {color: gray, border: 1px solid gray;}")
        self.ui.lineEditEmailNewEntry.setStyleSheet("QLineEdit {color: gray, border 1px solid gray;}")
        self.ui.lineEditPasswordNewEntry.setStyleSheet("QLineEdit {color: gray, border: 1px solid gray;}")
        self.ui.lineEditPinNewEntry.setStyleSheet("QLineEdit {color: gray, border: 1px solid gray;}")
        self.ui.lineEditNotesNewEntry.setStyleSheet("QLineEdit {color: gray, border: 1px solid gray;}")

        self.ui.tableWidgetLoginData.clearSelection()
        
    def ExitEditDeleteUI(self):
        self.ui.pushButtonEdit.setVisible(True)
        self.ui.pushButtonDelete.setVisible(True)
        self.ui.pushButtonCancel.setVisible(False)
        self.ui.pushButtonConfirm.setVisible(False)
        
        self.ui.lineEditNameSearch.setEnabled(True)
        self.ui.lineEditEmailSearch.setEnabled(True)
        self.ui.lineEditNameNewEntry.setEnabled(True)
        self.ui.lineEditUsernameNewEntry.setEnabled(True)
        self.ui.lineEditEmailNewEntry.setEnabled(True)
        self.ui.lineEditPasswordNewEntry.setEnabled(True)
        self.ui.pushButtonGenSecPass.setEnabled(True)
        self.ui.lineEditPinNewEntry.setEnabled(True)
        self.ui.lineEditNotesNewEntry.setEnabled(True)
        self.ui.pushButtonAddNewEntry.setEnabled(True)
        self.ui.pushButtonExportData.setEnabled(True)

        self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        self.ui.lineEditUsernameNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        self.ui.lineEditEmailNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        self.ui.lineEditPasswordNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        self.ui.lineEditPinNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        self.ui.lineEditNotesNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        
        self.ui.tableWidgetLoginData.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)

        self.ui.label_tableInstructions.setText("")


    def OnEdit(self, clearStatusBar=True):
        if clearStatusBar:
            self.ClearStatusBar()
        self.EnterEditDeleteUI()
        self.ui.label_tableInstructions.setText("Make the changes you want to the cells, then press Confirm to save")
        self.ui.tableWidgetLoginData.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.action = "Edit"

    def OnConfirm(self):
        self.ExitEditDeleteUI()

        if self.action == "Edit":
            self.ApplyEdits()
        elif self.action == "Delete":
            self.DeleteRows()

        self.ui.tableWidgetLoginData.clearSelection()

    def OnCancel(self):
        self.ExitEditDeleteUI()

        if self.action == "Edit":
            self.DisplayTable()

        self.ui.tableWidgetLoginData.clearSelection()
        self.ClearStatusBar()

    def OnDelete(self):
        self.ClearStatusBar()
        self.EnterEditDeleteUI()
        self.ui.label_tableInstructions.setText("Select the rows you want to delete, then press Confirm to save")
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
            self.UpdateStatusBar("Name can't be empty!", "red")
            self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid red;}")
            return

        if self.loginData.isin(newEntryData).all(axis=1).any():
            self.UpdateStatusBar("Failed to add entry. This is a duplicate entry that already exists")
            return
        
        newEntryDF = pd.DataFrame(newEntryData)
        self.loginData = pd.concat([self.loginData, newEntryDF], ignore_index = True)

        self.ClearFields()     
        self.UpdateStatusBar("New entry added")
        self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.DisplayTable()
        self.SaveData()

    def ClearFields(self):
        self.ui.lineEditNameNewEntry.setText("")
        self.ui.lineEditUsernameNewEntry.setText("")
        self.ui.lineEditEmailNewEntry.setText("")
        self.ui.lineEditPasswordNewEntry.setText("")
        self.ui.lineEditPinNewEntry.setText("")
        self.ui.lineEditNotesNewEntry.setText("")


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

        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            item = self.ui.tableWidgetLoginData.item(row, 0)
            if item:
                item.setBackground(QtGui.QColor(255, 228, 196))  # Bisque color

        self.ui.tableWidgetLoginData.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: lightblue; color: black; }")


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

        updatedDataFrame = pd.DataFrame(updatedData, columns = ['Name', 'Username', 'Email', 'Password', 'Pin', 'Notes'])       
        if (updatedDataFrame.iloc[:, 0].str.strip() == "").any():
            self.UpdateStatusBar("Name can't be blank", "red")
            self.OnEdit(False)
        else:
            mismatch = (self.loginData != updatedDataFrame)
            mismatchCount = mismatch.sum().sum()

            self.loginData = updatedDataFrame

            if mismatchCount == 0:
                self.UpdateStatusBar("No cells edited")
            elif mismatchCount == 1:
                self.UpdateStatusBar("1 cell edited")
            else:
                self.UpdateStatusBar(str(mismatchCount) + " cells edited")

            self.SaveData()
            self.DisplayTable()


    def DeleteRows(self):
        selectedRows = set()
        for item in self.ui.tableWidgetLoginData.selectedItems():
            selectedRows.add(item.row())
        selectedRows = sorted(selectedRows, reverse = True)

        self.loginData = self.loginData.drop(index = selectedRows)

        for row in selectedRows:
            self.ui.tableWidgetLoginData.removeRow(row)

        if len(selectedRows) == 0:
            self.UpdateStatusBar("No entries deleted")
        elif len(selectedRows) == 1:
            self.UpdateStatusBar("1 entry deleted")
        else:
            self.UpdateStatusBar(str(len(selectedRows)) + " entries deleted")
        self.SaveData()


    def OnGeneratePassword(self):
        self.ClearStatusBar()
        PasswordObj = PasswordGenerator()
        self.ui.lineEditPasswordNewEntry.setText(PasswordObj.GetPassword())
        if PasswordObj.GetPassword() != "":
            self.UpdateStatusBar("Password generated")


    def UpdateStatusBar(self, message, color="black"):
        self.status_bar.setStyleSheet("QStatusBar{ color: " + color + "; }")
        self.status_bar.showMessage(message)
        print(message)
    
    def ClearStatusBar(self):
        self.status_bar.clearMessage()


class ImportFileOptions(QtWidgets.QDialog):
    dialogClosed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Create Password Generator Dialog
        self.Dialog = QtWidgets.QDialog()
        self.ui = ImportFileOptionsGUI.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()


    def AdditionalUISetup(self):
        self.ui.radioButtonImportAdd.clicked.connect(self.OnRadioButtonToggled)
        self.ui.radioButtonImportReplace.clicked.connect(self.OnRadioButtonToggled)
        self.ui.radioButtonImportAdd.click()

    def ConnectButtons(self):
        self.ui.pushButtonImportConfirm.clicked.connect(self.OnConfirm)
        self.ui.pushButtonImportCancel.clicked.connect(self.OnCancel)

    def OnRadioButtonToggled(self):
        if self.ui.radioButtonImportAdd.isChecked():
            self.ui.labelImportDesc.setText("This will only add new, unique entries from the selected file to your login data")
        elif self.ui.radioButtonImportReplace.isChecked():
            self.ui.labelImportDesc.setText("This will replace all your current login data with the new data from the selected file")

        
    def OnConfirm(self):
        if self.ui.radioButtonImportAdd.isChecked():
            self.dialogClosed.emit("Add")
        elif self.ui.radioButtonImportReplace.isChecked():
            self.dialogClosed.emit("Replace")
        self.CloseDialog()

    def OnCancel(self):
        self.dialogClosed.emit("Cancel")
        self.CloseDialog()    
        
    def CloseDialog(self):
        self.Dialog.close()


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
        self.ui = GeneratePasswordGUI.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()
        self.GeneratePassword()

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

        # If the password will contain symbols but not numbers
        elif self.ui.checkBoxPwdIncludeSymbols.isChecked():
            numSymbols = min(self.sys_random.randint(1, length // 2.5), length - 2)
            remainingChars -= numSymbols
            randSymbols = self.sys_random.choices(self.specialSymbols, k = numSymbols)
            password = randSymbols
        
        password += self.sys_random.choices(self.uppercaseLetters + self.lowercaseLetters, k = remainingChars)

        # Shuffle the password order. Doesn't make it any more random
        self.sys_random.shuffle(password)

        # If there is a length mismatch, which should not happen
        if (len(password) != length):
            print ("Error length mismatch! Expected: " + str(length) + "  Actual: " + str(len(password)))

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
