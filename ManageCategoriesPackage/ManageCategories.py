import functools
import json
import logging
import os
import sys
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import QColorDialog, QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

from . import ManageCategoriesGUI

# python -m PyQt6.uic.pyuic -x ManageCategories.ui -o ManageCategoriesGUICopy.py

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
class ManageCategoriesClass(QDialog):
    # Signals
    updatedCategoriesSignal = pyqtSignal(dict, dict)

    # Global constants
    LOGGER = logging.getLogger()
    if getattr(sys, 'frozen', False): #Running as an executable
        CATEGORY_CONFIG_PATH = os.path.join(sys.executable, "Data", "CategoryConfig.json")
    else: # Running as a script
        CATEGORY_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Data", "CategoryConfig.json")

    # Global dynamic variables
    number_of_categories = 0
    indexed_original_category_data = {}
    category_index = 0
    default_category_color = ""

    def __init__(self, categoryData, defaultCategoryColor):
        super().__init__()

        # Create Manage Categories dialogs
        self.Dialog = QDialog()
        self.ui = ManageCategoriesGUI.Ui_DialogManageCategories()
        self.ui.setupUi(self.Dialog)
        self.AdditionalUISetup()
        self.ConnectButtons()
        self.SetupCategoryRows(categoryData)
        self.default_category_color = defaultCategoryColor

    def AdditionalUISetup(self):
        self.ui.labelErrorMessage.setVisible(False)
        self.ui.labelErrorMessage.setStyleSheet("QLabel {color: red}")
        self.ui.verticalLayoutCategories.setAlignment(Qt.AlignmentFlag.AlignTop)

    def ConnectButtons(self):
        self.ui.pushButtonAddNew.clicked.connect(lambda _: self.OnAddNew())
        self.ui.pushButtonCancel.clicked.connect(lambda _: self.OnCancel())
        self.ui.pushButtonConfirm.clicked.connect(lambda _: self.OnConfirm())


    def SetupCategoryRows(self, categoryData):
        for name, color in categoryData.items():
            self.category_index += 1
            self.indexed_original_category_data[self.category_index] = {"Name": name, "Color": color}
            self.InsertCategoryRow(self.indexed_original_category_data[self.category_index]["Name"], self.indexed_original_category_data[self.category_index]["Color"])

    def InsertCategoryRow(self, categoryName, color):
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setProperty("Index", self.category_index)

        color = QColor(color)
        labelColorSquare = QLabel()
        labelColorSquare.setFixedSize(30, 30)
        labelColorSquare.setProperty("Color", color.name())
        labelColorSquare.setStyleSheet(f"QLabel {{background-color: {color.name()}; border: 1px solid black;}}")
        labelColorSquare.setCursor(Qt.CursorShape.PointingHandCursor)
        labelColorSquare.mousePressEvent = lambda event, color=color, label=labelColorSquare: self.OpenColorPicker(event, color, label)
        horizontal_layout.addWidget(labelColorSquare)

        lineEditCategory = QLineEdit()
        lineEditCategory.setFixedHeight(30)
        lineEditCategory.setStyleSheet("QLineEdit {font-size: 18px;}")
        lineEditCategory.setText(categoryName)
        horizontal_layout.addWidget(lineEditCategory)

        pushButtonRemove = QPushButton("Remove")
        pushButtonRemove.setFixedSize(80, 30)
        horizontal_layout.addWidget(pushButtonRemove)
        pushButtonRemove.clicked.connect(lambda: self.deleteRow(horizontal_layout))

        self.ui.verticalLayoutCategories.addLayout(horizontal_layout)
        QTimer.singleShot(10, lambda: {self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())})

    def OpenColorPicker(self, event: QMouseEvent, color, label):
        color = QColorDialog.getColor(color)
        if color.isValid():
            label.setStyleSheet(f"QLabel {{background-color: {color.name()}; border: 1px solid black;}}")
            label.setProperty("Color", color.name())


    def OnAddNew(self):
        self.category_index += 1
        self.InsertCategoryRow("", self.default_category_color)
    
    def deleteRow(self, layout):
        for col in range(layout.count()):
            widget = layout.itemAt(col).widget()
            if widget: widget.deleteLater()
        layout.deleteLater()


    def OnConfirm(self):
        updatedCategoryNames = []
        updatedCategoryData = {}
        emptyCategoryFound = False
        invalidCategories = set()
        for i in range(self.ui.verticalLayoutCategories.count()):
            horizontalLayout = self.ui.verticalLayoutCategories.itemAt(i)
            horizontalLayout.itemAt(1).widget().setStyleSheet("QLineEdit {font-size: 18px;}")
            index = horizontalLayout.property("Index")
            color = horizontalLayout.itemAt(0).widget().property("Color")
            name = horizontalLayout.itemAt(1).widget().text()

            if name == "":
                emptyCategoryFound = True
                horizontalLayout.itemAt(1).widget().setStyleSheet("QLineEdit {font-size: 18px; border: 2px solid red;}")
            elif name.lower() == "select all":
                invalidCategories.add("'" + name + "'")
                horizontalLayout.itemAt(1).widget().setStyleSheet("QLineEdit {font-size: 18px; border: 2px solid red;}")
            if name.title() not in updatedCategoryNames:
                updatedCategoryData[index] = {"Name": name.title(), "Color": color}
                updatedCategoryNames.append(name.title())
            else:
                self.LOGGER.warning("Ignoring duplicate category name (case insensitive): %s", name)

        errorMessage = "Category names cannot be "
        if emptyCategoryFound and invalidCategories:
            errorMessage = "Category names cannot be "
            invalidCategories = ["empty"] + list(invalidCategories)
            errorMessage += ", ".join(map(str, invalidCategories[:-1])) + " or " + str(invalidCategories[-1]) + "!"
        elif emptyCategoryFound:
            errorMessage = "Category names cannot be empty!"
        elif invalidCategories:
            errorMessage = "Category names cannot be "
            invalidCategories = list(invalidCategories)
            errorMessage += ", ".join(map(str, invalidCategories[:-1])) + " or " + str(invalidCategories[-1]) + "!"
        if emptyCategoryFound or invalidCategories:
            self.ui.labelErrorMessage.setText(errorMessage)
            self.ui.labelErrorMessage.setVisible(True)
            self.LOGGER.warning("Failed to save categories. %s", errorMessage)
            return

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

        if len(newEntries) > 0:
            self.LOGGER.info("Added these new categories to the category config: %s", newEntries)
        if len(differenceMap) > 0:
            self.LOGGER.info("Category data updated with these changes: %s", differenceMap)
        if len(differenceMap) + len(newEntries) > 0:
            try:
                with open(self.CATEGORY_CONFIG_PATH, "w+") as configFile:
                    json.dump(noIndexUpdatedCategoryData, configFile, indent=4)
                self.LOGGER.info("Category config file saved: %s", self.CATEGORY_CONFIG_PATH)
            except IOError as e:
                self.LOGGER.error("Exception saving category config file:", exc_info=True)
                return
            self.updatedCategoriesSignal.emit(differenceMap, noIndexUpdatedCategoryData)
        else:
            self.LOGGER.info("No categories were updated")
        self.Dialog.close()

    def OnCancel(self):
        self.CloseDialog()    
        
    def CloseDialog(self):
        self.Dialog.close()
