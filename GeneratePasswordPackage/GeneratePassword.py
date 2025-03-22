import functools
import logging
import random
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QDialog

from . import GeneratePasswordGUI

# python -m PyQt6.uic.pyuic -x GeneratePassword.ui -o GeneratePasswordGUICopy.py

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
class GeneratePasswordClass(QDialog):
    # Signals
    passwordCopiedSignal = pyqtSignal(str)

    # Global constants
    LOWERCASE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    UPPERCASE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    SPECIAL_SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', '[', ']', '{', '}', '<', '>']
    LOGGER = logging.getLogger()
    SYS_RANDOM = random.SystemRandom()

    def __init__(self, preferences):
        super().__init__()

        # Create Password Generator dialog
        self.Dialog = QDialog()
        self.ui = GeneratePasswordGUI.Ui_DialogGeneratePassword()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup(preferences)
        self.ConnectButtons()
        self.GeneratePassword()


    def AdditionalUISetup(self, preferences):
        self.ui.labelPwdOptions.setStyleSheet("QLabel {font-size: 16px;}")
        self.ui.labelPwdCopiedtoClipboard.setVisible(False)
        self.ui.spinBoxPwdLen.setValue(preferences["DefaultPasswordOptions"]["Length"])
        self.ui.checkBoxPwdIncludeNumbers.setChecked(preferences["DefaultPasswordOptions"]["IncludeNumbers"])
        self.ui.checkBoxPwdIncludeSymbols.setChecked(preferences["DefaultPasswordOptions"]["IncludeSymbols"])


    def ConnectButtons(self):
        self.ui.pushButtonPwdGeneratePwd.clicked.connect(lambda _: self.GeneratePassword())
        self.ui.pushButtonPwdCancel.clicked.connect(lambda _: self.OnCancel())
        self.ui.pushButtonPwdOK.clicked.connect(lambda _: self.OnOK())

    def GeneratePassword(self):
        password = []
        length = self.ui.spinBoxPwdLen.value()
        remainingChars = length

        # If the password will contain numbers
        if self.ui.checkBoxPwdIncludeNumbers.isChecked():
            numNumbers = self.SYS_RANDOM.randint(1, length // 2.5)
            # If the password will contain numbers and symbols
            if self.ui.checkBoxPwdIncludeSymbols.isChecked():
                numSymbols = min(self.SYS_RANDOM.randint(1, length // 2.5), length - 3)
                remainingChars -= numSymbols
                randSymbols = self.SYS_RANDOM.choices(self.SPECIAL_SYMBOLS, k = numSymbols)
                password = randSymbols

                numNumbers = min(numNumbers, remainingChars - 2)

            remainingChars -= numNumbers
            password += self.SYS_RANDOM.choices(self.NUMBERS, k = numNumbers)

        # If the password will contain symbols but not numbers
        elif self.ui.checkBoxPwdIncludeSymbols.isChecked():
            numSymbols = min(self.SYS_RANDOM.randint(1, length // 2.5), length - 2)
            remainingChars -= numSymbols
            randSymbols = self.SYS_RANDOM.choices(self.SPECIAL_SYMBOLS, k = numSymbols)
            password = randSymbols
        
        password += self.SYS_RANDOM.choices(self.UPPERCASE_LETTERS + self.LOWERCASE_LETTERS, k = remainingChars)
        self.SYS_RANDOM.shuffle(password)
        self.ui.lineEditPwdPassword.setText(''.join(password))

        # Copy password to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.lineEditPwdPassword.text())
        self.ui.labelPwdCopiedtoClipboard.setVisible(True)
        self.ui.lineEditPwdPassword.selectAll()

        self.LOGGER.info("Generated password with: length=%d | includeNumbers=%s | includeSymbols=%s | password=%s", 
                         len(password), self.ui.checkBoxPwdIncludeNumbers.isChecked(), self.ui.checkBoxPwdIncludeSymbols.isChecked(), ''.join(password))

    def OnOK(self):
        self.passwordCopiedSignal.emit(self.ui.lineEditPwdPassword.text())
        self.CloseDialog()

    def OnCancel(self):
        self.CloseDialog()

    def CloseDialog(self):
        self.Dialog.close()