import json
import os
import pandas as pd
import re
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QAbstractItemView, QComboBox, QFileDialog, QMainWindow, QStatusBar, QTableWidget, QTableWidgetItem

from PasswordManagerGUI import *
import GeneratePasswordPackage.GeneratePassword as GeneratePassword
import ImportFileOptionsPackage.ImportFileOptions as ImportFileOptions
import ManageCategoriesPackage.ManageCategories as ManageCategories

# python -m PyQt6.uic.pyuic -x PasswordManager.ui -o PasswordManagerGUICopy.py
# python -m PyInstaller --onefile --noconsole --distpath ~/Documents PasswordManager.py

class PasswordManager():
    # Global constants
    CATEGORY_COLUMN = 0
    NAME_COLUMN = 1
    EMAIL_COLUMN = 3
    PASSWORD_COLUMN = 4
    CATEGORY_SELECT_ALL = "Select All"
    EXPECTED_COLUMNS = ['Category', 'Name', 'Username', 'Email', 'Password', 'Pin', 'Notes']
    if getattr(sys, 'frozen', False): #Running as an executable
        LOGIN_DATA_PATH = os.path.join(sys._MEIPASS, "Data", "Login_data.parquet")
        CATEGORY_CONFIG_PATH = os.path.join(sys._MEIPASS, "Data", "CategoryConfig.json")
    else: # Running as a script
        LOGIN_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "Login_data.parquet")
        CATEGORY_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "CategoryConfig.json")
    DEFAULT_CATEGORY_COLOR = "#e6e6e6"

    # Global dynamic variables
    login_data = pd.DataFrame()
    imported_data = pd.DataFrame()
    edit_delete_action = ""
    category_data = {}
    show_passwords = False

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
        self.ReadCategories()
        self.AddMissingCategories()
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
        self.ui.lineEditFilterName.textChanged.connect(self.OnFilterData)
        self.ui.lineEditFilterEmail.textChanged.connect(self.OnFilterData)

        self.ui.checkBoxShowPasswords.stateChanged.connect(self.OnShowPasswords)

        self.status_bar = QStatusBar()
        self.MainWindow.setStatusBar(self.status_bar)


    def ConnectButtons(self):
        self.ui.pushButtonClearFilters.clicked.connect(self.OnClearFilters)
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


    def ReadCategories(self):
        importedData = {}
        try:
            with open(self.CATEGORY_CONFIG_PATH) as configFile:
                importedData = json.load(configFile)
        except Exception as e:
            print(e)
        
        for name, color in importedData.items():
            colorHexPattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            if not color or not bool(re.match(colorHexPattern, color)):
                importedData[name] = self.DEFAULT_CATEGORY_COLOR

        self.category_data = importedData

    
    def FillComboBoxes(self):
        self.ui.comboBoxFilterCategory.clear()
        self.ui.comboBoxFilterCategory.addItems(sorted(self.category_data.keys()))
        self.ui.comboBoxFilterCategory.insertItem(0, self.CATEGORY_SELECT_ALL)
        self.ui.comboBoxFilterCategory.setCurrentIndex(0)

        self.ui.comboBoxCategoryNewEntry.clear()
        self.ui.comboBoxCategoryNewEntry.addItems(sorted(self.category_data.keys()))
        self.ui.comboBoxCategoryNewEntry.insertItem(0, "")
        self.ui.comboBoxCategoryNewEntry.setCurrentIndex(0)


    def GetData(self):
        if os.path.isfile(self.LOGIN_DATA_PATH):
            loginDataFile = pd.read_parquet(self.LOGIN_DATA_PATH)
            missingColumns = set(self.EXPECTED_COLUMNS) - set(loginDataFile.columns)
            if len(missingColumns) > 0:
                self.UpdateStatusBar("Data file is malformed, attempting to fix.", "red")
                for col in missingColumns:
                    loginDataFile[col] = ""
            loginDataFile = loginDataFile[self.EXPECTED_COLUMNS]
            loginDataFile = loginDataFile.fillna("")
            self.login_data = loginDataFile
        else:
            self.login_data = pd.DataFrame(columns = self.EXPECTED_COLUMNS)

        
    def SaveData(self):
        self.login_data.to_parquet("./Data/Login_Data.parquet", index = False)


    def OnClearFilters(self):
        self.ui.comboBoxFilterCategory.setCurrentIndex(0)
        self.ui.lineEditFilterName.setText("")
        self.ui.lineEditFilterEmail.setText("")
        self.UpdateStatusBar("Filters cleared")


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
                
        self.imported_data = self.imported_data[self.EXPECTED_COLUMNS]
        self.imported_data = self.imported_data.fillna("")

        importFileObj = ImportFileOptions.ImportFileOptionsClass()
        importFileObj.dialogClosedSignal.connect(self.HandleImportFileDialogClosed)
        importFileObj.Dialog.exec()

    def HandleImportFileDialogClosed(self, response):
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
            category = category.title()
            if category not in self.category_data and category != '':
                self.category_data[category] = self.DEFAULT_CATEGORY_COLOR
                anyCategoryAdded = True

        if anyCategoryAdded:
            print("Added")
            try:
                with open(self.CATEGORY_CONFIG_PATH, "w+") as configFile:
                    json.dump(self.category_data, configFile, indent=4)
            except IOError as e:
                print(e)


    def OnFilterData(self):
        categoryFilter = self.ui.comboBoxFilterCategory.currentText().lower()
        nameFilter = self.ui.lineEditFilterName.text().lower()
        emailFilter = self.ui.lineEditFilterEmail.text().lower()

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
        categoriesObj = ManageCategories.ManageCategoriesClass(self.category_data)
        categoriesObj.differenceMapSignal.connect(self.HandleDifferenceMap)
        categoriesObj.updatedDataSignal.connect(self.HandleUpdatedData)
        categoriesObj.Dialog.exec()

    def HandleDifferenceMap(self, differenceMap):
        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            categoryCell = self.ui.tableWidgetLoginData.item(row, self.CATEGORY_COLUMN)
            if categoryCell.text() in differenceMap:
                if differenceMap[categoryCell.text()]["Action"] == "Edit":
                    categoryCell.setText(differenceMap[categoryCell.text()]["NewName"])
                    categoryCell.setBackground(QColor(differenceMap[categoryCell.text()]["NewColor"]))
                elif differenceMap[categoryCell.text()]["Action"] == "Delete":
                    categoryCell.setText("")
                    categoryCell.setBackground(QColor(self.DEFAULT_CATEGORY_COLOR))

    def HandleUpdatedData(self, updatedData):
        self.category_data = updatedData
        self.FillComboBoxes()


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


    def OnShowPasswords(self):
        self.show_passwords = self.ui.checkBoxShowPasswords.isChecked()
        passwords = self.login_data.iloc[:, self.PASSWORD_COLUMN].tolist()
        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            self.ui.tableWidgetLoginData.item(row, self.PASSWORD_COLUMN).setText(self.ShowOrHidePassword(passwords[row]))

    def ShowOrHidePassword(self, password):
            if self.show_passwords:
                return password
            return "*" * len(password)
            

    def EnterEditDeleteUI(self):
        self.ui.pushButtonEdit.setVisible(False)
        self.ui.pushButtonDelete.setVisible(False)
        self.ui.pushButtonCancel.setVisible(True)
        self.ui.pushButtonConfirm.setVisible(True)
        
        self.ui.checkBoxShowPasswords.setDisabled(True)
        self.ui.comboBoxFilterCategory.setDisabled(True)
        self.ui.lineEditFilterName.setDisabled(True)
        self.ui.lineEditFilterEmail.setDisabled(True)
        self.ui.lineEditNameNewEntry.setDisabled(True)
        self.ui.lineEditUsernameNewEntry.setDisabled(True)
        self.ui.lineEditEmailNewEntry.setDisabled(True)
        self.ui.lineEditPasswordNewEntry.setDisabled(True)
        self.ui.lineEditPinNewEntry.setDisabled(True)
        self.ui.lineEditNotesNewEntry.setDisabled(True)
        self.ui.pushButtonClearFilters.setDisabled(True)
        self.ui.pushButtonManageCategories.setDisabled(True)
        self.ui.pushButtonRemoveDuplicates.setDisabled(True)
        self.ui.pushButtonImportData.setDisabled(True)
        self.ui.pushButtonExportData.setDisabled(True)
        self.ui.pushButtonGenSecPass.setDisabled(True)
        self.ui.pushButtonAddNewEntry.setDisabled(True)

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
        
        self.ui.checkBoxShowPasswords.setEnabled(True)
        self.ui.comboBoxFilterCategory.setEnabled(True)
        self.ui.lineEditFilterName.setEnabled(True)
        self.ui.lineEditFilterEmail.setEnabled(True)
        self.ui.lineEditNameNewEntry.setEnabled(True)
        self.ui.lineEditUsernameNewEntry.setEnabled(True)
        self.ui.lineEditEmailNewEntry.setEnabled(True)
        self.ui.lineEditPasswordNewEntry.setEnabled(True)
        self.ui.lineEditPinNewEntry.setEnabled(True)
        self.ui.lineEditNotesNewEntry.setEnabled(True)
        self.ui.pushButtonClearFilters.setEnabled(True)
        self.ui.pushButtonManageCategories.setEnabled(True)
        self.ui.pushButtonRemoveDuplicates.setEnabled(True)
        self.ui.pushButtonImportData.setEnabled(True)
        self.ui.pushButtonExportData.setEnabled(True)
        self.ui.pushButtonGenSecPass.setEnabled(True)
        self.ui.pushButtonAddNewEntry.setEnabled(True)

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
            comboBox.addItems(sorted(self.category_data.keys()))
            originalCategory = self.ui.tableWidgetLoginData.item(row, self.CATEGORY_COLUMN)
            comboBox.setCurrentText(originalCategory.text())
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
            self.UpdateStatusBar("Failed to add entry. This is a duplicate entry that already exists", "red")
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
                stringData = str(dataList[row][col])
                qTableWidgetItem = QTableWidgetItem(stringData)
                if col == self.CATEGORY_COLUMN:
                    qTableWidgetItem.setText(stringData.title())
                    if qTableWidgetItem.text() in self.category_data:
                        qTableWidgetItem.setBackground(QColor(self.category_data[qTableWidgetItem.text()]))
                    else:
                        qTableWidgetItem.setBackground(QColor(self.DEFAULT_CATEGORY_COLOR))
                elif col == self.NAME_COLUMN:
                    qTableWidgetItem.setBackground(QColor(255, 228, 196))  # Bisque color
                elif col == self.PASSWORD_COLUMN:
                    qTableWidgetItem.setData(Qt.ItemDataRole.UserRole, stringData)
                    qTableWidgetItem.setText(self.ShowOrHidePassword(qTableWidgetItem.data(Qt.ItemDataRole.UserRole)))

                self.ui.tableWidgetLoginData.setItem(row, col, qTableWidgetItem)


        self.ui.tableWidgetLoginData.repaint()
        self.ui.tableWidgetLoginData.resizeColumnsToContents()
        
        if self.LastColumnFits():
            self.ui.tableWidgetLoginData.horizontalHeader().setSectionResizeMode(self.ui.tableWidgetLoginData.columnCount() - 1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.tableWidgetLoginData.horizontalHeader().setStretchLastSection(True)

        self.ui.tableWidgetLoginData.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: lightblue; color: black; }")


    def ApplyEdits(self):       
        updatedData = []
        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            rowData = []
            for col in range(self.ui.tableWidgetLoginData.columnCount()):
                item = self.ui.tableWidgetLoginData.item(row, col)
                cellData = item.text()
                if col == self.PASSWORD_COLUMN:
                    if re.match("\*+", cellData):
                        cellData = item.data(Qt.ItemDataRole.UserRole)
                    else:
                        item.setData(Qt.ItemDataRole.UserRole, item.text())
                rowData.append(cellData)
            updatedData.append(rowData)

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
        passwordObj = GeneratePassword.GeneratePasswordClass()
        passwordObj.Dialog.exec()

        self.ui.lineEditPasswordNewEntry.setText(passwordObj.GetPassword())
        if passwordObj.GetPassword() != "":
            self.UpdateStatusBar("Password generated")


    def UpdateStatusBar(self, message, color="black"):
        self.status_bar.setStyleSheet("QStatusBar{ color: " + color + "; }")
        self.status_bar.showMessage(message)
        print(message)
    
    def ClearStatusBar(self):
        self.status_bar.clearMessage()


if __name__ == "__main__":
    passMngr = PasswordManager()
