from random import SystemRandom
import sys
from PasswordManagerGUI import *
import pandas as pd
from PyQt6 import QtCore, QtGui, QtWidgets
import os.path

# python -m PyQt6.uic.pyuic -x PasswordManager.ui -o PasswordManagerGUI.py

class PasswordManager():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.AdditionalUISetup()
        self.ConnectButtons()

        self.loginData = pd.DataFrame(columns = ['Name', 'Username', 'Email', 'Password', 'Pin', 'Notes'])
        self.GetData()
        self.DisplayTable()

        sys.exit(app.exec())


    def AdditionalUISetup(self):
        pushButtonAddNewEntryFont = self.ui.pushButtonAddNewEntry.font()
        pushButtonAddNewEntryFont.setPointSize(16)
        self.ui.pushButtonAddNewEntry.setFont(pushButtonAddNewEntryFont)

        self.ui.pushButtonCancel.setVisible(False)
        self.ui.pushButtonSave.setVisible(False)



    def ConnectButtons(self):
        #self.ui.pushButtonSearch.clicked.connect()
        #self.ui.pushButtonClear.clicked.connect()
        self.ui.pushButtonAddNewEntry.clicked.connect(self.AddNewEntry)
        self.ui.pushButtonEdit.clicked.connect(self.OnEdit)
        #self.ui.pushButtonDelete.clicked.connect()
        self.ui.pushButtonSave.clicked.connect(self.SaveEdits)
        #self.ui.pushButtonCancel.clicked.connect()
        self.ui.pushButtonExportData.clicked.connect(self.ExportData)
        self.ui.pushButtonGenSecPass.clicked.connect(self.GeneratePassword)


    def GetData(self):
        if os.path.isfile("./Login_Data.pkl"):
            self.loginData = pd.read_pickle("./Login_Data.pkl")
        
    def SaveData(self):
        self.loginData.to_pickle("./Login_Data.pkl")

    def ExportData(self):
        self.loginData.to_excel("./Login_Data.xlsx", index=False)


    def OnEdit(self):
        self.ui.pushButtonEdit.setVisible(False)
        self.ui.pushButtonDelete.setVisible(False)
        self.ui.pushButtonCancel.setVisible(True)
        self.ui.pushButtonSave.setVisible(True)

        self.ui.tableWidgetLoginData.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)


    def SaveEdits(self):
        self.ui.pushButtonEdit.setVisible(True)
        self.ui.pushButtonDelete.setVisible(True)
        self.ui.pushButtonCancel.setVisible(False)
        self.ui.pushButtonSave.setVisible(False)

        self.ui.tableWidgetLoginData.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.ApplyEdits()

    
    def AddNewEntry(self):
        # Perform checks that the necessary fields are filled in
        
        newEntryData = {
                        'Name': [self.ui.lineEditNameNewEntry.text()],
                        'Username': [self.ui.lineEditUsernameNewEntry.text()],
                        'Email': [self.ui.lineEditEmailNewEntry.text()],
                        'Password': [self.ui.lineEditPasswordNewEntry.text()],
                        'Pin': [self.ui.lineEditPinNewEntry.text()],
                        'Notes': [self.ui.lineEditNotesNewEntry.text()]
                       }
        
        if newEntryData['Name'][0].strip() == '':
            print("Name can't be empty")
            return

        newEntryDF = pd.DataFrame(newEntryData)
        
        self.loginData = pd.concat([self.loginData, newEntryDF], ignore_index = True)

        self.DisplayTable()
        self.SaveData()


    def _lastColumnFits(self):
        total_width = self.ui.tableWidgetLoginData.viewport().width()
        column_width_sum = 0

        for column in range(self.ui.tableWidgetLoginData.columnCount()):
            column_width_sum += self.ui.tableWidgetLoginData.horizontalHeader().sectionSize(column)

        return total_width >= column_width_sum
    
    def DisplayTable(self):
        print("Displaying")
        self.ui.tableWidgetLoginData.setRowCount(self.loginData.shape[0])
        self.ui.tableWidgetLoginData.setColumnCount(self.loginData.shape[1])
        self.ui.tableWidgetLoginData.setHorizontalHeaderLabels(self.loginData.columns)        

        dataList = self.loginData.values.tolist()
        for row in range(len(dataList)):
            for col in range(len(dataList[0])):
                self.ui.tableWidgetLoginData.setItem(row, col, QtWidgets.QTableWidgetItem(str(dataList[row][col])))

        self.ui.tableWidgetLoginData.repaint()

        self.ui.tableWidgetLoginData.resizeColumnsToContents()
        
        if self._lastColumnFits():
            self.ui.tableWidgetLoginData.horizontalHeader().setSectionResizeMode(self.ui.tableWidgetLoginData.columnCount() - 1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.tableWidgetLoginData.horizontalHeader().setStretchLastSection(True)


    def ApplyEdits(self):
        print("Applying edits")
        
        numRows = self.ui.tableWidgetLoginData.rowCount()
        numColumns = self.ui.tableWidgetLoginData.columnCount()

        updatedData = []

        for row in range(numRows):
            row_data = []
            for col in range(numColumns):
                item = self.ui.tableWidgetLoginData.item(row, col)
                if item:
                    row_data.append(item.text())
            updatedData.append(row_data)

        self.loginData = pd.DataFrame(updatedData, columns = ['Name', 'Username', 'Email', 'Password', 'Pin', 'Notes'])

        self.SaveData()
        self.DisplayTable()


    def GeneratePassword(self):
        # Open new password window

        PasswordObj = PasswordGenerator()
        password = PasswordObj.generatePassword(10, True, True)
        self.ui.lineEditPasswordNewEntry.setText(password)



class PasswordGenerator():
    def __init__(self):
        # All possible characters in a password
        self.lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.specialSymbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', '[', ']', '{', '}', '<', '>']

        # Cryptographically secure randomizer
        self.sys_random = SystemRandom()

    def generatePassword(self, length, includeSymbols, includeNumbers):
        password = []

        # Passwords must be at least 4 characters long
        if length < 4:
            print("Error")
            return -1

        remainingChars = length

        # If the password will contain numbers
        if includeNumbers:
            numNumbers = self.sys_random.randint(1, length // 2.5)
            # If the password will contain numbers and symbols
            if includeSymbols:
                numSymbols = min(self.sys_random.randint(1, length // 2.5), length - 3)
                remainingChars -= numSymbols
                randSymbols = self.sys_random.choices(self.specialSymbols, k = numSymbols)
                password = randSymbols

                numNumbers = min(numNumbers, remainingChars - 2)


            remainingChars -= numNumbers
            password += self.sys_random.choices(self.numbers, k = numNumbers)
            
            numUppercase = self.sys_random.randint(1, remainingChars - 1)
            remainingChars -= numUppercase

        # If the password will contain symbols but not numbers
        elif includeSymbols:
            numSymbols = min(self.sys_random.randint(1, length // 2.5), length - 2)
            remainingChars -= numSymbols
            randSymbols = self.sys_random.choices(self.specialSymbols, k = numSymbols)
            password = randSymbols

            numUppercase = self.sys_random.randint(1, remainingChars - 1)
            remainingChars -= numUppercase

        # If the password will only contain letters
        else:
            numUppercase = self.sys_random.randint(1, length - 1)
            remainingChars -= numUppercase

        # Choose uppercase letters
        password += self.sys_random.choices(self.uppercaseLetters, k = numUppercase)
        # Choose lowercase letters
        password += self.sys_random.choices(self.lowercaseLetters, k = remainingChars)

        # Shuffle the password order
        self.sys_random.shuffle(password)

        # If there is a length mismatch, which should not happen
        if (len(password) != length):
            print ("Error length mismatch: " + str(len(password)) + " v.s. " + str(length))

        # Return the password as a string
        return ''.join(password)


if __name__ == "__main__":
    passMngr = PasswordManager()
