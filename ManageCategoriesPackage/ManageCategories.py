import json
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import QColorDialog, QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

from . import ManageCategoriesGUI

class ManageCategoriesClass(QDialog):
    # Signals
    differenceMapSignal = pyqtSignal(dict)
    newEntriesSignal = pyqtSignal(list)
    updatedDataSignal = pyqtSignal(dict)

    # Global constants
    CATEGORY_CONFIG_PATH = "./Data/CategoryConfig.json"
    DEFAULT_CATEGORY_COLOR = "#e6e6e6"

    # Global dynamic variables
    number_of_categories = 0
    indexed_original_category_data = {}
    category_index = 0

    def __init__(self, categoryData):
        super().__init__()

        # Create Manage Categories dialogs
        self.Dialog = QDialog()
        self.ui = ManageCategoriesGUI.Ui_DialogManageCategories()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()
        self.SetupCategoryRows(categoryData)

    def AdditionalUISetup(self):
        self.ui.labelErrorMessage.setVisible(False)
        self.ui.verticalLayoutCategories.setAlignment(Qt.AlignmentFlag.AlignTop)

    def ConnectButtons(self):
        self.ui.pushButtonAddNew.clicked.connect(self.OnAddNew)
        self.ui.pushButtonCancel.clicked.connect(self.OnCancel)
        self.ui.pushButtonConfirm.clicked.connect(self.OnConfirm)




    def SetupCategoryRows(self, categoryData):
        for name, color in categoryData.items():
            self.category_index += 1
            self.indexed_original_category_data[self.category_index] = {"Name": name, "Color": color}
            self.InsertCategoryRow(self.indexed_original_category_data[self.category_index]["Name"], self.indexed_original_category_data[self.category_index]["Color"])

    
    def InsertCategoryRow(self, categoryName, color):
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setProperty("Index", self.category_index)

        labelColorSquare = self.CreateColorSquare(color)
        horizontal_layout.addWidget(labelColorSquare)

        lineEditCategory = QLineEdit()
        lineEditCategory.setFixedHeight(30)
        lineEditCategory.setStyleSheet("QLineEdit { font-size: 18px; }")
        lineEditCategory.setText(categoryName)
        horizontal_layout.addWidget(lineEditCategory)

        pushButtonRemove = QPushButton("Remove")
        pushButtonRemove.setFixedSize(80, 30)
        horizontal_layout.addWidget(pushButtonRemove)
        pushButtonRemove.clicked.connect(lambda: self.deleteRow(horizontal_layout))

        self.ui.verticalLayoutCategories.addLayout(horizontal_layout)
        QTimer.singleShot(10, lambda: {self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())})
        self.number_of_categories += 1

    def CreateColorSquare(self, color):
        color = QColor(color)
        colorSquare = QLabel()
        colorSquare.setFixedSize(30, 30)
        colorSquare.setProperty("Color", color.name())
        colorSquare.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
        colorSquare.setCursor(Qt.CursorShape.PointingHandCursor)
        colorSquare.mousePressEvent = lambda event, color=color, label=colorSquare: self.OpenColorPicker(event, color, label)
        return colorSquare

    def OpenColorPicker(self, event: QMouseEvent, color, label):
        color = QColorDialog.getColor(color)
        if color.isValid():
            label.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            label.setProperty("Color", color.name())


    def OnAddNew(self):
        self.category_index += 1
        self.InsertCategoryRow("", self.DEFAULT_CATEGORY_COLOR)
    
    def deleteRow(self, layout):
        for col in range(layout.count()):
            widget = layout.itemAt(col).widget()
            if widget: widget.deleteLater()
        layout.deleteLater()


    def SaveToCategoryConfigFile(self):
        categoryData = {}
        #for row in range(self.ui.verticalLayoutCategories.count()):



    def OnConfirm(self):
        updatedCategoryData = {}
        for i in range(self.ui.verticalLayoutCategories.count()):
            horizontalLayout = self.ui.verticalLayoutCategories.itemAt(i)
            index = horizontalLayout.property("Index")
            color = horizontalLayout.itemAt(0).widget().property("Color")
            name = horizontalLayout.itemAt(1).widget().text().title()
            if name == "" or name == "Select All":
                print("TODO: make layout red, print error")
                # TODO: Highlight error row, display error message
                return
                
            updatedCategoryData[index] = {"Name": name, "Color": color}

        differenceMap = {}
        newEntries = []
        for key in self.indexed_original_category_data.keys() - updatedCategoryData.keys():
            differenceMap[self.indexed_original_category_data[key]["Name"]] = {"Action": "Delete"}

        for key in updatedCategoryData.keys() - self.indexed_original_category_data.keys():
            newEntries.append((updatedCategoryData[key]["Name"], updatedCategoryData[key]["Color"]))
        
        # Keys in both but with different values
        for key in self.indexed_original_category_data.keys() & updatedCategoryData.keys():
            if self.indexed_original_category_data[key] != updatedCategoryData[key]:
                differenceMap[self.indexed_original_category_data[key]["Name"]] = {"Action": "Edit", "NewName": updatedCategoryData[key]["Name"], "NewColor": updatedCategoryData[key]["Color"]}

        noIndexUpdatedCategoryData = {value["Name"]: value["Color"] for value in updatedCategoryData.values()}
        try:
            with open(self.CATEGORY_CONFIG_PATH, "w+") as configFile:
                json.dump(noIndexUpdatedCategoryData, configFile, indent=4)
        except IOError as e:
            print(e)
            return

        if len(differenceMap) > 0:
            self.differenceMapSignal.emit(differenceMap)

        self.updatedDataSignal.emit(noIndexUpdatedCategoryData)
        self.Dialog.close()

    def OnCancel(self):
        print("Cancel")
        #self.dialogClosed.emit("Cancel")
        self.CloseDialog()    
        
    def CloseDialog(self):
        self.Dialog.close()
