from random import SystemRandom
import sys
from PasswordManagerGUI import *
import GeneratePasswordGUI
import ImportFileOptionsGUI
import pandas as pd
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableWidget, QTableWidgetItem, QFileDialog, QStatusBar, QComboBox
from PyQt6.QtCore import pyqtSignal
import os

# python -m PyQt6.uic.pyuic -x PasswordManager.ui -o PasswordManagerGUICopy.py
# python -m PyInstaller --onefile --noconsole --distpath ~/Documents PasswordManager.py

class PasswordManager():
    # Global constants
    CATEGORY_COLUMN = 0
    NAME_COLUMN = 1
    EMAIL_COLUMN = 3
    CATEGORY_SELECT_ALL = "Select All"
    EXPECTED_COLUMNS = ['Category', 'Name', 'Username', 'Email', 'Password', 'Pin', 'Notes']

    # Global dynamic variables
    category_list = []
    login_data = pd.DataFrame()
    imported_data = pd.DataFrame()
    edit_delete_action = ""


    def __init__(self):
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.AdditionalUISetup()
        self.ConnectButtons()
        
        app.processEvents()

        self.GetData()
        self.AddMissingCategories()
        self.FillCategoryList()
        self.FillComboBoxes()
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

        self.ui.comboBoxFilterCategory.currentIndexChanged.connect(self.OnFilterData)
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
        self.ui.pushButtonManageCategories.clicked.connect(self.OnManageCategories)


    def FillCategoryList(self):
        # TODO: Read from a category file
        self.category_list.sort()

    
    def FillComboBoxes(self):
        self.ui.comboBoxFilterCategory.addItems(self.category_list)
        self.ui.comboBoxFilterCategory.insertItem(0, self.CATEGORY_SELECT_ALL)
        self.ui.comboBoxFilterCategory.setCurrentIndex(0)

        self.ui.comboBoxCategoryNewEntry.addItems(self.category_list)
        self.ui.comboBoxCategoryNewEntry.insertItem(0, "")
        self.ui.comboBoxFilterCategory.setCurrentIndex(0)


    def GetData(self):
        if os.path.isfile("./Login_Data.parquet"):
            self.login_data = pd.read_parquet("./Login_Data.parquet")
            # TODO: Check for data quality. Fill in missing columns with blank, drop extra columns
        else:
            self.login_data = pd.DataFrame(columns = self.EXPECTED_COLUMNS)

        
    def SaveData(self):
        self.login_data.to_parquet("./Login_Data.parquet", index = False)


    def OnImportData(self):
        self.ClearStatusBar()
        fileObj = QFileDialog.getOpenFileName(None, "Open File", "", 
                                              """All Supported Formats (*.xlsx; *.csv; *.json; *.xml; *.parquet);;
                                              Excel (*.xlsx);;
                                              CSV (*.csv);;
                                              JSON (*.json);;
                                              XML (*.xml);;
                                              Parquet (*.parquet);;
                                              All Files (*)""")
        if fileObj[0] == "":
            return
        
        self.imported_data = None
        fileType = os.path.splitext(fileObj[0])[1]
        match fileType:
            case ".xlsx":
                self.imported_data = pd.read_excel(fileObj[0], dtype=str)
            case ".csv":
                self.imported_data = pd.read_csv(fileObj[0], dtype=str)
            case ".json":
                self.imported_data = pd.read_json(fileObj[0], dtype=str)
            case ".xml":
                self.imported_data = pd.read_xml(fileObj[0], dtype=str)
            case ".parquet":
                self.imported_data = pd.read_parquet(fileObj[0])
            case _:
                self.UpdateStatusBar(f"Invalid file selected, '{fileType}' is not a valid file type", "red")
                return
            
        # TODO: For missing columns, fill with blank. Error on additional columns
        # Check if the columns match up
        if set(self.EXPECTED_COLUMNS) != set(self.imported_data.columns):
            missingColumns = set(self.EXPECTED_COLUMNS) - set(self.imported_data.columns)
            extraColumns = set(self.imported_data.columns) - set(self.EXPECTED_COLUMNS)
            statusBarMessage = "Error importing data."
            if len(missingColumns) > 0:
                statusBarMessage += " Missing columns: [" + ", ".join(missingColumns) + "]."
            if len(extraColumns) > 0:
                statusBarMessage += " Unexpected columns: [" + ", ".join(missingColumns) + "]."
            self.UpdateStatusBar(statusBarMessage, "red")
            return
                
        self.imported_data = self.imported_data.fillna("")

        importFileObj = ImportFileOptions()
        importFileObj.dialogClosed.connect(self.OnImportFileDialogClosed)
        importFileObj.Dialog.exec()

    def OnImportFileDialogClosed(self, response):
        if response == "Cancel":
            return
        elif response == "Add":
            self.login_data = pd.concat([self.login_data, self.imported_data])
            self.login_data = self.login_data.drop_duplicates()
            self.UpdateStatusBar('Data imported with the "Add" mode')
        elif response == "Replace":
            self.login_data = self.imported_data
            self.UpdateStatusBar('Data imported with the "Replace" mode')

        self.AddMissingCategories()
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
                self.login_data.to_excel(fileObj[0], index = False)
                self.UpdateStatusBar(".xlsx file exported")
            case ".csv":
                self.login_data.to_csv(fileObj[0], index = False)
                self.UpdateStatusBar(".csv file exported")
            case ".json":
                self.login_data.to_json(fileObj[0], index = False)
                self.UpdateStatusBar(".json file exported")
            case ".xml":
                self.login_data.to_xml(fileObj[0], index = False)
                self.UpdateStatusBar(".xml file exported")
            case ".parquet":
                self.login_data.to_parquet(fileObj[0], index = False)
                self.UpdateStatusBar(".parquet file exported")
            case _:
                self.UpdateStatusBar(f"Invalid file selected, '{fileType}' is not a valid file type", "red")


    def AddMissingCategories(self):
        anyCategoryAdded = False
        for category in self.login_data['Category']:
            if category not in self.category_list and category != '':
                self.category_list.append(category)
                anyCategoryAdded = True

        if anyCategoryAdded:
            # TODO: Update category file
            ...


    def OnFilterData(self):
        categoryFilter = self.ui.comboBoxFilterCategory.currentText().lower()
        nameFilter = self.ui.lineEditNameSearch.text().lower()
        emailFilter = self.ui.lineEditEmailSearch.text().lower()

        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            itemCategory = self.ui.tableWidgetLoginData.item(row, self.CATEGORY_COLUMN)
            itemName = self.ui.tableWidgetLoginData.item(row, self.NAME_COLUMN)
            itemEmail = self.ui.tableWidgetLoginData.item(row, self.EMAIL_COLUMN)

            itemCategoryText = itemCategory.text().lower() if itemCategory else ''
            itemNameText = itemName.text().lower() if itemName else ''
            itemEmailText = itemEmail.text().lower() if itemEmail else ''

            if (categoryFilter == itemCategoryText or categoryFilter == self.CATEGORY_SELECT_ALL.lower()) and (nameFilter in itemNameText) and (emailFilter in itemEmailText):
                self.ui.tableWidgetLoginData.setRowHidden(row, False)
            else:
                self.ui.tableWidgetLoginData.setRowHidden(row, True)

        
    def OnManageCategories(self):
        print("Manage categories")


    def OnRemoveDuplicates(self):
        oldDataFrame = self.login_data
        self.login_data = oldDataFrame.drop_duplicates()

        duplicatesDropped = oldDataFrame.shape[0] - self.login_data.shape[0]
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
        self.edit_delete_action = "Edit"

        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            comboBox = QComboBox()
            comboBox.addItems(self.category_list)
            self.ui.tableWidgetLoginData.setCellWidget(row, self.CATEGORY_COLUMN, comboBox)

    def OnConfirm(self):
        self.ExitEditDeleteUI()

        if self.edit_delete_action == "Edit":
            for row in range(self.ui.tableWidgetLoginData.rowCount()):
                comboBox = self.ui.tableWidgetLoginData.cellWidget(row, self.CATEGORY_COLUMN)
                categoryValue = comboBox.currentText()
                self.ui.tableWidgetLoginData.removeCellWidget(row, self.CATEGORY_COLUMN)
                self.ui.tableWidgetLoginData.setItem(row, self.CATEGORY_COLUMN, QTableWidgetItem(categoryValue))
            self.ApplyEdits()
        elif self.edit_delete_action == "Delete":
            self.DeleteRows()

        self.ui.tableWidgetLoginData.clearSelection()

    def OnCancel(self):
        self.ExitEditDeleteUI()

        if self.edit_delete_action == "Edit":
            for row in range(self.ui.tableWidgetLoginData.rowCount()):
                comboBox = self.ui.tableWidgetLoginData.cellWidget(row, self.CATEGORY_COLUMN)
                categoryValue = comboBox.currentText()
                self.ui.tableWidgetLoginData.removeCellWidget(row, self.CATEGORY_COLUMN)
                self.ui.tableWidgetLoginData.setItem(row, self.CATEGORY_COLUMN, QTableWidgetItem(categoryValue))
            self.DisplayTable()

        self.ui.tableWidgetLoginData.clearSelection()
        self.ClearStatusBar()

    def OnDelete(self):
        self.ClearStatusBar()
        self.EnterEditDeleteUI()
        self.ui.label_tableInstructions.setText("Select the rows you want to delete, then press Confirm to save")
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.edit_delete_action = "Delete"

    
    def OnAddNewEntry(self):       
        newEntryData = {
                        'Category': [self.ui.comboBoxCategoryNewEntry.currentText()],
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

        if self.login_data.isin(newEntryData).all(axis=1).any():
            self.UpdateStatusBar("Failed to add entry. This is a duplicate entry that already exists")
            return
        
        newEntryDF = pd.DataFrame(newEntryData)
        self.login_data = pd.concat([self.login_data, newEntryDF], ignore_index = True)

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
        self.ui.tableWidgetLoginData.setRowCount(self.login_data.shape[0])
        self.ui.tableWidgetLoginData.setColumnCount(self.login_data.shape[1])
        self.ui.tableWidgetLoginData.setHorizontalHeaderLabels(self.login_data.columns)        

        dataList = self.login_data.values.tolist()
        for row in range(len(dataList)):
            for col in range(len(dataList[0])):
                self.ui.tableWidgetLoginData.setItem(row, col, QTableWidgetItem(str(dataList[row][col])))

        self.ui.tableWidgetLoginData.repaint()
        self.ui.tableWidgetLoginData.resizeColumnsToContents()
        
        if self.LastColumnFits():
            self.ui.tableWidgetLoginData.horizontalHeader().setSectionResizeMode(self.ui.tableWidgetLoginData.columnCount() - 1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.tableWidgetLoginData.horizontalHeader().setStretchLastSection(True)

        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            item = self.ui.tableWidgetLoginData.item(row, self.NAME_COLUMN)
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

        updatedDataFrame = pd.DataFrame(updatedData, columns = self.EXPECTED_COLUMNS)

        if (updatedDataFrame.iloc[:, self.NAME_COLUMN].str.strip() == "").any():
            self.UpdateStatusBar("Name can't be blank", "red")
            self.OnEdit(False)
        else:
            mismatch = (self.login_data != updatedDataFrame)
            mismatchCount = mismatch.sum().sum()

            self.login_data = updatedDataFrame

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

        self.login_data = self.login_data.drop(index = selectedRows)
        self.login_data = self.login_data.reset_index(drop = True)

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
