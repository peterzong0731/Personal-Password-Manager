import datetime
import functools
import json
import logging
import os
import pandas as pd
import pytz
import re
import sys
import threading
import webbrowser
from PyQt6.QtCore import QStandardPaths, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QAbstractItemView, QComboBox, QFileDialog, QMainWindow, QStatusBar, QTableWidget, QTableWidgetItem

from PasswordManagerGUI import *
import GeneratePasswordPackage.GeneratePassword as GeneratePassword
import ImportFileOptionsPackage.ImportFileOptions as ImportFileOptions
import LoggerSetup
import ManageCategoriesPackage.ManageCategories as ManageCategories
import ManageDataBackups
import MenuBarPackage.ManagePreferences as ManagePreferences


# python -m PyQt6.uic.pyuic -x PasswordManager.ui -o PasswordManagerGUICopy.py
# python -m PyInstaller --onefile --noconsole --distpath . --name PersonalPasswordManager PasswordManager.py

# TODO: Add preference color selection feature
# TODO: Themes
# TODO: Add preference to change time zone

def log_function_call(func):
    """Decorator to log function calls with arguments and return values."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling: {func.__name__}()")
        logging.debug(f"Calling : {func.__name__}() | Args: {args} | Kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

def log_all_methods(cls):
    """Class decorator to log all method calls."""
    ignoredFunctions = ["ShowOrHidePassword"]
    for attr_name, attr in cls.__dict__.items():
        if callable(attr) and not attr_name.startswith("__") and attr_name not in ignoredFunctions:
            setattr(cls, attr_name, log_function_call(attr))
    return cls

@log_all_methods
class PasswordManager():
    # Global constants
    DOCUMENTS_FOLDER_PATH = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
    CATEGORY_COLUMN = 0
    NAME_COLUMN = 1
    EMAIL_COLUMN = 2
    PASSWORD_COLUMN = 4
    PIN_COLUMN = 5
    LAST_MODIFIED_COLUMN = 6
    CATEGORY_SELECT_ALL = "Select All"
    EXPECTED_COLUMNS = ['Category', 'Name', 'Email', 'Username/ID', 'Password', 'Pin', 'Last Modified', 'Notes']
    if getattr(sys, 'frozen', False): #Running as an executable
        LOGIN_DATA_PATH = os.path.join(os.getenv('APPDATA'), "PersonalPasswordManager", "Data", "Login_data.parquet")
        CATEGORY_CONFIG_PATH = os.path.join(os.getenv('APPDATA'), "PersonalPasswordManager", "Data", "CategoryConfig.json")
        PREFERENCES_PATH = os.path.join(os.getenv('APPDATA'), "PersonalPasswordManager", "Data", "Preferences.json")
        LOG_FILE_FOLDER = os.path.join(os.getenv('APPDATA'), "PersonalPasswordManager", "Logs")
    else: # Running as a script
        LOGIN_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "Login_data.parquet")
        CATEGORY_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "CategoryConfig.json")
        PREFERENCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "Preferences.json")
        LOG_FILE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
    LOG_FILE_PATH = os.path.join(LOG_FILE_FOLDER, "PasswordManager.log")

    # Global dynamic variables
    login_data = pd.DataFrame()
    imported_data = pd.DataFrame()
    edit_delete_action = ""
    category_data = {}
    show_passwords = False
    logger = None
    preferences = {}

    def __init__(self):
        LoggerSetup.LoggerSetupClass().setupLogger()
        self.logger = logging.getLogger()
        self.logger.info("--------------------------------------------------------------")
        self.logger.info("Application launched")
        
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.AdditionalUISetup()
        self.ConnectButtons()
        
        app.processEvents()

        self.GetData()
        self.ReadPreferencesFromFile()
        self.ReadCategories()
        self.AddMissingCategories()
        self.FillComboBoxes()
        self.DisplayTable()
        self.ManageDataBackups()

        self.logger.info("Application loaded")

        sys.exit(app.exec())


    def AdditionalUISetup(self):
        pushButtonAddNewEntryFont = self.ui.pushButtonAddNewEntry.font()
        pushButtonAddNewEntryFont.setPointSize(16)
        self.ui.pushButtonAddNewEntry.setFont(pushButtonAddNewEntryFont)

        self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditEmailNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.lineEditUsernameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
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

        self.ui.comboBoxFilterCategory.currentIndexChanged.connect(lambda _: self.OnFilterData())
        self.ui.lineEditFilterName.textChanged.connect(lambda _: self.OnFilterData())
        self.ui.lineEditFilterEmail.textChanged.connect(lambda _: self.OnFilterData())

        self.ui.checkBoxShowPasswords.stateChanged.connect(lambda _:self.OnShowPasswords())

        self.status_bar = QStatusBar()
        self.MainWindow.setStatusBar(self.status_bar)


    def ConnectButtons(self):
        self.ui.pushButtonClearFilters.clicked.connect(lambda _: self.OnClearFilters())
        self.ui.pushButtonAddNewEntry.clicked.connect(lambda _: self.OnAddNewEntry())
        self.ui.pushButtonEdit.clicked.connect(lambda _: self.OnEdit())
        self.ui.pushButtonDelete.clicked.connect(lambda _: self.OnDelete())
        self.ui.pushButtonConfirm.clicked.connect(lambda _: self.OnConfirm())
        self.ui.pushButtonCancel.clicked.connect(lambda _: self.OnCancel())
        self.ui.pushButtonImportData.clicked.connect(lambda _: self.OnImportData())
        self.ui.pushButtonExportData.clicked.connect(lambda _: self.OnExportData())
        self.ui.pushButtonGenSecPass.clicked.connect(lambda _: self.OnGeneratePassword())
        self.ui.pushButtonRemoveDuplicates.clicked.connect(lambda _: self.OnRemoveDuplicates())
        self.ui.pushButtonManageCategories.clicked.connect(lambda _: self.OnManageCategories())
        self.ui.actionPreferences.triggered.connect(lambda _: self.OnMenuSettingsPreferences())
        self.ui.actionViewReadMe.triggered.connect(lambda _: self.OnMenuHelpReadme())


    def OnMenuHelpReadme(self):
        webbrowser.open("https://github.com/peterzong0731/Personal-Password-Manager/blob/main/README.md")

    def OnMenuSettingsPreferences(self):
        managePreferencesObj = ManagePreferences.ManagePreferencesClass(self.preferences)
        managePreferencesObj.applyPreferencesSignal.connect(self.ApplyPreferences)
        managePreferencesObj.Dialog.exec()

    def ReadPreferencesFromFile(self):
        preferencesData = {
            "Theme": "Light",
            "HidePasswordsByDefault": True,
            "TableHeaderRowColor": "#a4a4a4",
            "TableNameColumnColor": "#cfe1ff",
            "DefaultCategoryColor": "#e6e6e6",
            "DefaultPasswordOptions": {
                "Length": 8,
                "IncludeNumbers": True,
                "IncludeSymbols": False
            }
        }
        try:
            with open(self.PREFERENCES_PATH) as preferencesFile:
                preferencesData = json.load(preferencesFile)
            self.logger.info('Preferences file loaded: "%s"', self.PREFERENCES_PATH)
        except Exception as e:
            self.logger.error("Exception reading preferences file:", exc_info=True)

        self.preferences = preferencesData
        self.ApplyPreferences(self.preferences)

    def ApplyPreferences(self, preferences):
        self.logger.info("Updated preferences: %s", preferences)
        self.preferences = preferences
        if preferences['Theme'].lower() == "light":
            self.ChangeToLightTheme()
        elif preferences["Theme"].lower() == "dark":
            self.ChangeToDarkTheme()
        self.ui.checkBoxShowPasswords.setChecked(not preferences["HidePasswordsByDefault"])
        self.DisplayTable()


    def ChangeToLightTheme(self):
        # TODO: Read from style sheet and update components
        ...

    def ChangeToDarkTheme(self):
        # TODO: Read from style sheet and update components
        ...


    def ManageDataBackups(self):
        try:
            backupsThread = threading.Thread(target = ManageDataBackups.ManageDataBackupsClass, args = (self.login_data,), daemon = True)
            backupsThread.start()
        except Exception as e:
            self.logger.error("Exception with ManageDataBackups:", exc_info=True)


    def ReadCategories(self):
        importedData = {}
        try:
            with open(self.CATEGORY_CONFIG_PATH) as configFile:
                importedData = json.load(configFile)
            self.logger.info('Category config file loaded: "%s"', self.CATEGORY_CONFIG_PATH)
        except Exception as e:
            self.logger.error("Exception reading category config file:", exc_info=True)
        
        for name, color in importedData.items():
            colorHexPattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            if not color or not bool(re.match(colorHexPattern, color)):
                importedData[name] = self.preferences["DefaultCategoryColor"]

        self.category_data = importedData

    
    def FillComboBoxes(self):
        self.ui.comboBoxFilterCategory.clear()
        self.ui.comboBoxFilterCategory.addItems([self.CATEGORY_SELECT_ALL] + sorted(self.category_data.keys()))

        self.ui.comboBoxCategoryNewEntry.clear()
        self.ui.comboBoxCategoryNewEntry.addItems([""] + sorted(self.category_data.keys()))


    def GetData(self):
        self.login_data = pd.DataFrame({col: pd.Series(dtype='str') for col in self.EXPECTED_COLUMNS})
        if os.path.isfile(self.LOGIN_DATA_PATH):
            loginDataFile = pd.read_parquet(self.LOGIN_DATA_PATH)
            missingColumns = set(self.EXPECTED_COLUMNS) - set(loginDataFile.columns)
            if len(missingColumns) > 0:
                self.logger.warning('Source data file "%s" is malformed, attempting to fix', self.LOGIN_DATA_PATH)
                self.UpdateStatusBar("Source data file is malformed, attempting to fix.", "red")
                for col in missingColumns:
                    loginDataFile[col] = ""
            loginDataFile = loginDataFile[self.EXPECTED_COLUMNS]
            loginDataFile = loginDataFile.fillna("")
            self.login_data = pd.concat([self.login_data, loginDataFile], ignore_index = True)
        else:
            self.logger.info("Source data file does not exist, creating empty file")
            self.SaveData()
        self.logger.info("Source data loaded")

        
    def SaveData(self):
        self.login_data.to_parquet(self.LOGIN_DATA_PATH, index = False)
        self.logger.info("Login data saved to: %s", self.LOGIN_DATA_PATH)


    def OnClearFilters(self):
        self.ui.comboBoxFilterCategory.setCurrentIndex(0)
        self.ui.lineEditFilterName.setText("")
        self.ui.lineEditFilterEmail.setText("")
        self.UpdateStatusBar("Filters cleared")
        self.logger.info("Filters cleared")


    def OnImportData(self):
        self.ClearStatusBar()
        fileObj = QFileDialog.getOpenFileName(None, "Open File", self.DOCUMENTS_FOLDER_PATH, 
                                              """All Supported Formats (*.xlsx; *.csv; *.json; *.xml; *.parquet);;
                                              Excel (*.xlsx);;
                                              CSV (*.csv);;
                                              JSON (*.json);;
                                              XML (*.xml);;
                                              Parquet (*.parquet);;
                                              All Files (*)""")
        if fileObj[0] == "":
            self.logger.info("No import data file selected, returning")
            return
        
        self.logger.info('Import data file selected: "%s"', fileObj[0])
        
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
                self.logger.warning('Invalid file selected, "%s" is not a supported file type', fileType)
                self.UpdateStatusBar(f'Invalid file selected, "{fileType}" is not a supported file type', "red")
                return
            
        if set(self.EXPECTED_COLUMNS) != set(self.imported_data.columns):
            missingColumns = set(self.EXPECTED_COLUMNS) - set(self.imported_data.columns)
            extraColumns = set(self.imported_data.columns) - set(self.EXPECTED_COLUMNS)
            statusBarMessage = "Error importing data."
            if len(missingColumns) > 0:
                statusBarMessage += " Missing columns: [" + ", ".join(missingColumns) + "]."
            if len(extraColumns) > 0:
                statusBarMessage += " Unexpected columns: [" + ", ".join(missingColumns) + "]."
            self.logger.warning(statusBarMessage)
            self.UpdateStatusBar(statusBarMessage, "red")
            return
                
        self.imported_data = self.imported_data[self.EXPECTED_COLUMNS]
        self.imported_data = self.imported_data.fillna("")

        importFileObj = ImportFileOptions.ImportFileOptionsClass()
        importFileObj.dialogClosedSignal.connect(self.HandleImportFileDialogClosed)
        importFileObj.Dialog.exec()

    def HandleImportFileDialogClosed(self, response):
        if response == "Cancel":
            self.logger.info("Import data canceled")
            return
        elif response == "Add":
            self.login_data = pd.concat([self.login_data, self.imported_data])
            self.login_data = self.login_data.drop_duplicates()
        elif response == "Replace":
            self.login_data = self.imported_data

        self.AddMissingCategories()
        self.DisplayTable()
        self.SaveData()
        self.logger.info('Data imported with the "%s" mode', response)
        self.UpdateStatusBar(f'Data imported with the "{response}" mode')

    def OnExportData(self):
        self.ClearStatusBar()
        defaultFileName = "LoginData.xlsx"
        fileObj =  QFileDialog.getSaveFileName(None, "Save File", os.path.join(self.DOCUMENTS_FOLDER_PATH, defaultFileName), "Excel (*.xlsx);;CSV (*.csv);;JSON (*.json);;XML (*.xml);;Parquet (*.parquet);;All Files (*)")
        if fileObj[0] == "":
            self.logger.info("No export data file selected, returning")
            return
        
        if os.path.exists(fileObj[0]):
            try:
                fd = os.open(fileObj[0], os.O_RDWR | os.O_EXCL)
                os.close(fd)
            except OSError:
                self.logger.error("Exception exporting data file:", exc_info=True)
                self.UpdateStatusBar("Failed to export file because it is currently in use. Please close it and try again.", "red")
                return

        fileType = os.path.splitext(fileObj[0])[1]
        match fileType:
            case ".xlsx":
                self.login_data.to_excel(fileObj[0], index = False)
            case ".csv":
                self.login_data.to_csv(fileObj[0], index = False)
            case ".json":
                self.login_data.to_json(fileObj[0], index = False)
            case ".xml":
                self.login_data.to_xml(fileObj[0], index = False)
            case ".parquet":
                self.login_data.to_parquet(fileObj[0], index = False)
            case _:
                self.logger.warning('Invalid file selected, "%s" is not a supported file type', fileType)
                self.UpdateStatusBar(f"Invalid file selected, '{fileType}' is not a valid file type", "red")
                return
        
        self.logger.info('Data file exported: "%s', fileObj[0])
        self.UpdateStatusBar(f"{fileType[1:].upper()} file exported")


    def AddMissingCategories(self):
        anyCategoryAdded = False
        for category in self.login_data['Category']:
            category = category.title()
            if category not in self.category_data and category != '':
                self.category_data[category] = self.preferences["DefaultCategoryColor"]
                anyCategoryAdded = True

        if anyCategoryAdded:
            try:
                with open(self.CATEGORY_CONFIG_PATH, "w+") as configFile:
                    json.dump(self.category_data, configFile, indent=4)
                self.logger.info("Updated category config file with missing categories")
            except IOError:
                self.logger.error("Exception updating category config file with missing categories:", exc_info=True)
        else:
            self.logger.info("No missing categories to add")


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
        self.logger.info("Filtered entries on: Category = '%s', Name = '%s', Email = '%s'", categoryFilter, nameFilter, emailFilter)

        
    def OnManageCategories(self):
        categoriesObj = ManageCategories.ManageCategoriesClass(self.category_data, self.preferences["DefaultCategoryColor"])
        categoriesObj.updatedCategoriesSignal.connect(self.HandleUpdateCategoriesDailogClosed)
        categoriesObj.Dialog.exec()

    def HandleUpdateCategoriesDailogClosed(self, differenceMap, updatedCategories):
        for row in range(len(self.login_data)):
            categoryText = self.login_data.iloc[row, self.CATEGORY_COLUMN]
            if categoryText in differenceMap:
                if differenceMap[categoryText]["Action"] == "Edit":
                    self.login_data.iloc[row, self.CATEGORY_COLUMN] = differenceMap[categoryText]["NewName"]
                elif differenceMap[categoryText]["Action"] == "Delete":
                    self.login_data.iloc[row, self.CATEGORY_COLUMN] = ""

        self.category_data = updatedCategories
        self.FillComboBoxes()
        self.DisplayTable()
        self.SaveData()


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
        
        if duplicatesDropped > 0:
            self.DisplayTable()
            self.SaveData()
        self.logger.info("%d duplicates removed", duplicatesDropped)


    def OnShowPasswords(self):
        self.show_passwords = self.ui.checkBoxShowPasswords.isChecked()
        passwords = self.login_data.iloc[:, self.PASSWORD_COLUMN].tolist()
        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            self.ui.tableWidgetLoginData.item(row, self.PASSWORD_COLUMN).setText(self.ShowOrHidePassword(passwords[row]))
        if self.show_passwords:
            self.logger.info("Showing all passwords")
        else:
            self.logger.info("Hiding all passwords")

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
        self.ui.lineEditEmailNewEntry.setDisabled(True)
        self.ui.lineEditUsernameNewEntry.setDisabled(True)
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
        self.ui.lineEditEmailNewEntry.setStyleSheet("QLineEdit {color: gray, border 1px solid gray;}")
        self.ui.lineEditUsernameNewEntry.setStyleSheet("QLineEdit {color: gray, border: 1px solid gray;}")
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
        self.ui.lineEditEmailNewEntry.setEnabled(True)
        self.ui.lineEditUsernameNewEntry.setEnabled(True)
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
        self.ui.lineEditEmailNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
        self.ui.lineEditUsernameNewEntry.setStyleSheet("QLineEdit {color: white, border: 1px solid gray;}")
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

        def _OnCategoryChanged(categoryText, comboBox):
            if categoryText in self.category_data:
                comboBox.setStyleSheet(f"QComboBox {{ background-color: {self.category_data[categoryText]}; }}")
            else:
                comboBox.setStyleSheet(f"QComboBox {{ background-color: {self.preferences['DefaultCategoryColor']}; }}")

        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            comboBox = QComboBox()
            comboBox.addItems([""] + sorted(self.category_data.keys()))
            originalCategory = self.ui.tableWidgetLoginData.item(row, self.CATEGORY_COLUMN)
            comboBox.currentTextChanged.connect(lambda text, cb=comboBox: _OnCategoryChanged(text, cb))
            comboBox.setCurrentText(originalCategory.text())
            _OnCategoryChanged(comboBox.currentText(), comboBox)
            self.ui.tableWidgetLoginData.setCellWidget(row, self.CATEGORY_COLUMN, comboBox)

            lastModified = self.ui.tableWidgetLoginData.item(row, self.LAST_MODIFIED_COLUMN)
            lastModified.setFlags(lastModified.flags() & ~Qt.ItemFlag.ItemIsEditable)
            lastModified.setBackground(QColor("#f0f0f0"))

    def OnDelete(self):
        self.ClearStatusBar()
        self.EnterEditDeleteUI()
        self.ui.label_tableInstructions.setText("Select the rows you want to delete, then press Confirm to save")
        self.ui.tableWidgetLoginData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.edit_delete_action = "Delete"

    def OnConfirm(self):
        self.ExitEditDeleteUI()

        if self.edit_delete_action == "Edit":
            for row in range(self.ui.tableWidgetLoginData.rowCount()):
                comboBox = self.ui.tableWidgetLoginData.cellWidget(row, self.CATEGORY_COLUMN)
                categoryValue = comboBox.currentText()
                self.ui.tableWidgetLoginData.removeCellWidget(row, self.CATEGORY_COLUMN)
                self.ui.tableWidgetLoginData.setItem(row, self.CATEGORY_COLUMN, QTableWidgetItem(categoryValue))
                self.ui.tableWidgetLoginData.item(row, self.LAST_MODIFIED_COLUMN).setBackground(QColor("#ffffff"))
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

    def ApplyEdits(self):       
        updatedData = []
        mismatchCount = 0
        for row in range(self.ui.tableWidgetLoginData.rowCount()):
            rowData = []
            mismatchFound = False
            for col in range(self.ui.tableWidgetLoginData.columnCount()):
                item = self.ui.tableWidgetLoginData.item(row, col)
                cellData = item.text()
                originalData = self.login_data.iloc[row, col]
                if col == self.PASSWORD_COLUMN:
                    if re.match("\*+", cellData):
                        cellData = item.data(Qt.ItemDataRole.UserRole)
                    else:
                        item.setData(Qt.ItemDataRole.UserRole, item.text())
                elif col == self.LAST_MODIFIED_COLUMN:
                    cellData = item.data(Qt.ItemDataRole.UserRole)
                if cellData != originalData:
                    mismatchFound = True
                    mismatchCount += 1
                rowData.append(cellData)

            if mismatchFound:
                rowData[self.LAST_MODIFIED_COLUMN] = str(datetime.datetime.now(pytz.utc))
            updatedData.append(rowData)

        updatedDataFrame = pd.DataFrame(updatedData, columns = self.EXPECTED_COLUMNS)

        if (updatedDataFrame.iloc[:, self.NAME_COLUMN].str.strip() == "").any():
            self.UpdateStatusBar("Name can't be blank", "red")
            self.OnEdit(False)
        else:
            self.login_data = updatedDataFrame

            if mismatchCount == 0:
                self.UpdateStatusBar("No cells edited")
            elif mismatchCount == 1:
                self.UpdateStatusBar("1 cell edited")
            else:
                self.UpdateStatusBar(str(mismatchCount) + " cells edited")
            
            if mismatchCount > 0:
                self.SaveData()
                self.DisplayTable()
            self.logger.info("Edited %d cells", mismatchCount)

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

        if len(selectedRows) > 0:
            self.SaveData()
        self.logger.info("Deleted %d entires", len(selectedRows))

    
    def FormatDateTimeWithTimezone(self, UTCDateTimeAsString):
        # Need to get timezone from preferences
        UTCDateTime = datetime.datetime.strptime(UTCDateTimeAsString, "%Y-%m-%d %H:%M:%S.%f%z")
        return UTCDateTime.astimezone(pytz.timezone('US/Eastern')).strftime("%#d/%#m/%y %#I:%M:%S %p")

    
    def OnAddNewEntry(self):
        newEntryData = {
                        'Category': [self.ui.comboBoxCategoryNewEntry.currentText()],
                        'Name': [self.ui.lineEditNameNewEntry.text()],
                        'Email': [self.ui.lineEditEmailNewEntry.text()],
                        'Username/ID': [self.ui.lineEditUsernameNewEntry.text()],
                        'Password': [self.ui.lineEditPasswordNewEntry.text()],
                        'Pin': [self.ui.lineEditPinNewEntry.text()],
                        'Last Modified': [str(datetime.datetime.now(pytz.utc))],
                        'Notes': [self.ui.lineEditNotesNewEntry.text()]
                       }
        
        if newEntryData['Name'][0].strip() == '':
            self.UpdateStatusBar("Name can't be empty!", "red")
            self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid red;}")
            self.logger.warning("Failed to add new entry, the name was empty")
            return

        if self.login_data.isin(newEntryData).all(axis=1).any():
            self.UpdateStatusBar("Failed to add new entry. This is a duplicate entry that already exists", "red")
            self.logger.warning("Failed to add new entry because it is a duplicate: %s", newEntryData)
            return
        
        newEntryDF = pd.DataFrame(newEntryData)
        self.login_data = pd.concat([self.login_data, newEntryDF], ignore_index = True)

        self.ui.lineEditNameNewEntry.setStyleSheet("QLineEdit {border: 1px solid gray;}")
        self.ui.comboBoxCategoryNewEntry.setCurrentIndex(0)
        self.ClearFields()     
        self.DisplayTable()
        self.SaveData()
        self.UpdateStatusBar("New entry added")
        self.logger.info("Added new entry: %s", newEntryData)

    def ClearFields(self):
        self.ui.lineEditNameNewEntry.setText("")
        self.ui.lineEditEmailNewEntry.setText("")
        self.ui.lineEditUsernameNewEntry.setText("")
        self.ui.lineEditPasswordNewEntry.setText("")
        self.ui.lineEditPinNewEntry.setText("")
        self.ui.lineEditNotesNewEntry.setText("")

    
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
                        qTableWidgetItem.setBackground(QColor(self.preferences["DefaultCategoryColor"]))
                elif col == self.NAME_COLUMN:
                    qTableWidgetItem.setBackground(QColor(self.preferences["TableNameColumnColor"]))
                elif col == self.PASSWORD_COLUMN:
                    qTableWidgetItem.setData(Qt.ItemDataRole.UserRole, stringData)
                    qTableWidgetItem.setText(self.ShowOrHidePassword(qTableWidgetItem.data(Qt.ItemDataRole.UserRole)))
                elif col == self.LAST_MODIFIED_COLUMN:
                    qTableWidgetItem.setData(Qt.ItemDataRole.UserRole, stringData)
                    qTableWidgetItem.setText(self.FormatDateTimeWithTimezone(stringData))

                self.ui.tableWidgetLoginData.setItem(row, col, qTableWidgetItem)


        self.ui.tableWidgetLoginData.repaint()
        self.ui.tableWidgetLoginData.resizeColumnsToContents()

        total_width = self.ui.tableWidgetLoginData.viewport().width()
        column_width_sum = 0
        for column in range(self.ui.tableWidgetLoginData.columnCount()):
            column_width_sum += self.ui.tableWidgetLoginData.horizontalHeader().sectionSize(column)
        
        if total_width >= column_width_sum:
            self.ui.tableWidgetLoginData.horizontalHeader().setSectionResizeMode(self.ui.tableWidgetLoginData.columnCount() - 1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.tableWidgetLoginData.horizontalHeader().setStretchLastSection(True)

        self.ui.tableWidgetLoginData.horizontalHeader().setStyleSheet(f"QHeaderView::section {{ background-color: {self.preferences['TableHeaderRowColor']}; color: black; }}")


    def OnGeneratePassword(self):
        self.ClearStatusBar()
        passwordObj = GeneratePassword.GeneratePasswordClass(self.preferences)
        passwordObj.passwordCopiedSignal.connect(self.HandleGeneratePasswordDialogClosed)
        passwordObj.Dialog.exec()

    def HandleGeneratePasswordDialogClosed(self, password):
        self.ui.lineEditPasswordNewEntry.setText(password)
        self.UpdateStatusBar("Password copied")


    def UpdateStatusBar(self, message, color="black"):
        self.status_bar.setStyleSheet("QStatusBar{ color: " + color + "; }")
        self.status_bar.showMessage(message)
        print(message)
    
    def ClearStatusBar(self):
        self.status_bar.clearMessage()


if __name__ == "__main__":
    passMngr = PasswordManager()
