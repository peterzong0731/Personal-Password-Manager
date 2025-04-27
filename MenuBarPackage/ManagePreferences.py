import functools
import json
import logging
import os
import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QDialog

from . import ManagePreferencesGUI

# python -m PyQt6.uic.pyuic -x ManagePreferences.ui -o ManagePreferencesGUICopy.py

def log_function_call(func):
    """Decorator to log function calls with arguments and return values."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling: {func.__name__}()")
        logging.debug(f"Calling: {func.__name__}() | Args: {args} | Kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

def log_all_methods(cls):
    """Class decorator to log all method calls."""
    for attr_name, attr in cls.__dict__.items():
        if callable(attr) and not attr_name.startswith("__") and not isinstance(attr, pyqtSignal):
            setattr(cls, attr_name, log_function_call(attr))
    return cls


@log_all_methods
class ManagePreferencesClass(QDialog):
    # Signals
    applyPreferencesSignal = pyqtSignal(dict)

    # Global constants
    LOGGER = logging.getLogger()
    if getattr(sys, 'frozen', False): #Running as an executable
        PREFERENCES_PATH = os.path.join(os.getenv('APPDATA'), "PersonalPasswordManager", "Data", "Preferences.json")
    else: # Running as a script
        PREFERENCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "Data", "Preferences.json")

    # Global dynamic variables
    preferences = {}

    def __init__(self, preferences):
        super().__init__()

        # Create Manage Preferences dialog
        self.Dialog = QDialog()
        self.ui = ManagePreferencesGUI.Ui_DialogManagePreferences()
        self.ui.setupUi(self.Dialog)
        self.preferences = preferences

        self.AdditionalUISetup()
        self.ConnectButtons()


    def AdditionalUISetup(self):
        self.ui.comboBoxTheme.addItems(["Light", "Dark"])
        if self.preferences["Theme"] == "Dark":
            self.ui.comboBoxTheme.setCurrentIndex(1)
        self.ui.checkBoxHidePasswordsByDefault.setChecked(self.preferences["HidePasswordsByDefault"])
        # TODO: Create component and set table header row color
        # TODO: Create component and set table name column color
        # TODO: Create component and set default category color
        self.ui.spinBoxDefaultPasswordLength.setValue(self.preferences["DefaultPasswordOptions"]["Length"])
        self.ui.checkBoxDefaultPasswordIncludeNumbers.setChecked(self.preferences["DefaultPasswordOptions"]["IncludeNumbers"])
        self.ui.checkBoxDefaultPasswordIncludeSymbols.setChecked(self.preferences["DefaultPasswordOptions"]["IncludeSymbols"])


    def ConnectButtons(self):
        self.ui.pushButtonApply.clicked.connect(lambda _: self.OnApply())
        self.ui.pushButtonCancel.clicked.connect(lambda _: self.OnCancel())

        
    def OnApply(self):
        self.preferences["Theme"] = self.ui.comboBoxTheme.currentText()
        self.preferences["HidePasswordsByDefault"] = self.ui.checkBoxHidePasswordsByDefault.isChecked()
        self.preferences["TableHeaderRowColor"] = "#a4a4a4" # TODO: Update to selected color
        self.preferences["TableNameColumnColor"] = "#cfe1ff" # TODO: Update to selected color
        self.preferences["DefaultCategoryColor"] = "#e6e6e6" # TODO: Update to selected color
        self.preferences["DefaultPasswordOptions"]["Length"] = self.ui.spinBoxDefaultPasswordLength.value()
        self.preferences["DefaultPasswordOptions"]["IncludeNumbers"] = self.ui.checkBoxDefaultPasswordIncludeNumbers.isChecked()
        self.preferences["DefaultPasswordOptions"]["IncludeSymbols"] = self.ui.checkBoxDefaultPasswordIncludeSymbols.isChecked()
        
        self.applyPreferencesSignal.emit(self.preferences)
        with open(self.PREFERENCES_PATH, 'w') as preferencesFile:
            json.dump(self.preferences, preferencesFile, indent=4)
            self.LOGGER.info('Preferences file saved: "%s"', self.PREFERENCES_PATH)
        self.CloseDialog()

    def OnCancel(self):
        self.CloseDialog()
        
    def CloseDialog(self):
        self.Dialog.close()
  