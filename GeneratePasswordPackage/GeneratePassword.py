import random
from PyQt6.QtWidgets import QApplication, QDialog

from . import GeneratePasswordGUI

class GeneratePasswordClass(QDialog):
    # Global constants
    LOWERCASE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    UPPERCASE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    SPECIAL_SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', '[', ']', '{', '}', '<', '>']

    # Cryptographically secure randomizer
    sys_random = random.SystemRandom()

    def __init__(self):
        super().__init__()

        # Create Password Generator dialog
        self.Dialog = QDialog()
        self.ui = GeneratePasswordGUI.Ui_DialogGeneratePassword()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()
        self.GeneratePassword()


    def AdditionalUISetup(self):
        labelOptionsFont = self.ui.labelPwdOptions.font()
        labelOptionsFont.setPointSize(16)
        self.ui.labelPwdOptions.setFont(labelOptionsFont)
        self.ui.labelPwdCopiedtoClipboard.setVisible(False)


    def ConnectButtons(self):
        self.ui.pushButtonPwdGeneratePwd.clicked.connect(self.GeneratePassword)
        self.ui.pushButtonPwdCancel.clicked.connect(self.OnCancel)
        self.ui.pushButtonPwdOK.clicked.connect(self.OnOK)

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
                randSymbols = self.sys_random.choices(self.SPECIAL_SYMBOLS, k = numSymbols)
                password = randSymbols

                numNumbers = min(numNumbers, remainingChars - 2)

            remainingChars -= numNumbers
            password += self.sys_random.choices(self.NUMBERS, k = numNumbers)

        # If the password will contain symbols but not numbers
        elif self.ui.checkBoxPwdIncludeSymbols.isChecked():
            numSymbols = min(self.sys_random.randint(1, length // 2.5), length - 2)
            remainingChars -= numSymbols
            randSymbols = self.sys_random.choices(self.SPECIAL_SYMBOLS, k = numSymbols)
            password = randSymbols
        
        password += self.sys_random.choices(self.UPPERCASE_LETTERS + self.LOWERCASE_LETTERS, k = remainingChars)

        # Shuffle the password order. Doesn't make it any more random
        self.sys_random.shuffle(password)

        # Save the password as a string
        self.ui.lineEditPwdPassword.setText(''.join(password))

        # Copy password to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.lineEditPwdPassword.text())
        self.ui.labelPwdCopiedtoClipboard.setVisible(True)
        self.ui.lineEditPwdPassword.selectAll()

    def GetPassword(self):
        return self.ui.lineEditPwdPassword.text()
    

    def OnOK(self):
        self.CloseDialog()

    def OnCancel(self):
        self.ui.lineEditPwdPassword.setText("")
        self.CloseDialog()

    def CloseDialog(self):
        self.Dialog.close()