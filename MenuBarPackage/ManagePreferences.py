import functools
import logging
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
    dialogClosedSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Create Manage Preferences dialog
        self.Dialog = QDialog()
        self.ui = ManagePreferencesGUI.Ui_DialogManagePreferences()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()


    def AdditionalUISetup(self):
        ...

    def ConnectButtons(self):
        ...

        
    def OnConfirm(self):
        self.CloseDialog()

    def OnCancel(self):
        self.dialogClosedSignal.emit("Cancel")
        self.CloseDialog()    
        
    def CloseDialog(self):
        self.Dialog.close()
  