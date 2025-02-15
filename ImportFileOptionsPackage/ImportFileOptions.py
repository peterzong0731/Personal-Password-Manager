import functools
import logging
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog

from . import ImportFileOptionsGUI

# python -m PyQt6.uic.pyuic -x ImportFileOptions.ui -o ImportFileOptionsGUICopy.py

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
class ImportFileOptionsClass(QDialog):
    # Signals
    dialogClosedSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Create Import File Options dialog
        self.Dialog = QDialog()
        self.ui = ImportFileOptionsGUI.Ui_DialogImportFileOptions()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()


    def AdditionalUISetup(self):
        self.ui.radioButtonImportAdd.clicked.connect(lambda _: self.OnRadioButtonToggled())
        self.ui.radioButtonImportReplace.clicked.connect(lambda _: self.OnRadioButtonToggled())
        self.ui.radioButtonImportAdd.click()

    def ConnectButtons(self):
        self.ui.pushButtonImportConfirm.clicked.connect(lambda _: self.OnConfirm())
        self.ui.pushButtonImportCancel.clicked.connect(lambda _: self.OnCancel())

    def OnRadioButtonToggled(self):
        if self.ui.radioButtonImportAdd.isChecked():
            self.ui.labelImportDesc.setText("This will only add new, unique entries from the selected file to your login data")
        elif self.ui.radioButtonImportReplace.isChecked():
            self.ui.labelImportDesc.setText("This will replace all your current login data with the new data from the selected file")

        
    def OnConfirm(self):
        if self.ui.radioButtonImportAdd.isChecked():
            self.dialogClosedSignal.emit("Add")
        elif self.ui.radioButtonImportReplace.isChecked():
            self.dialogClosedSignal.emit("Replace")
        self.CloseDialog()

    def OnCancel(self):
        self.dialogClosedSignal.emit("Cancel")
        self.CloseDialog()    
        
    def CloseDialog(self):
        self.Dialog.close()
  