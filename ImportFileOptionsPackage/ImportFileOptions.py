from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog

from . import ImportFileOptionsGUI

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
            self.dialogClosedSignal.emit("Add")
        elif self.ui.radioButtonImportReplace.isChecked():
            self.dialogClosedSignal.emit("Replace")
        self.CloseDialog()

    def OnCancel(self):
        self.dialogClosedSignal.emit("Cancel")
        self.CloseDialog()    
        
    def CloseDialog(self):
        self.Dialog.close()
  