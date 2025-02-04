import datetime
import glob
import os
import pandas as pd
import sys
import threading

class ManageDataBackupsClass():
    # Global constants
    MAX_BACKUP_FILES_PER_FORMAT = 10
    if getattr(sys, 'frozen', False): #Running as an executable
        DATA_BACKUPS_FOLDER_PATH = os.path.join(sys._MEIPASS, "Data_Backups")
    else: # Running as a script
        DATA_BACKUPS_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data_Backups")

    def __init__(self, loginData: pd.DataFrame):
        if not os.path.isdir(self.DATA_BACKUPS_FOLDER_PATH):
            os.makedirs(self.DATA_BACKUPS_FOLDER_PATH)
        self.SaveBackup(loginData)
        self.CleanupBackupsFolder()

    def SaveBackup(self, loginData: pd.DataFrame):
        currentDateTime = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        loginData.to_csv(os.path.join(self.DATA_BACKUPS_FOLDER_PATH, f"Login_Data_Backup_{currentDateTime}.csv"), index = False)
        loginData.to_parquet(os.path.join(self.DATA_BACKUPS_FOLDER_PATH, f"Login_Data_Backup_{currentDateTime}.parquet"), index = False)

    def CleanupBackupsFolder(self):
        parquetFiles = sorted(glob.glob(os.path.join(self.DATA_BACKUPS_FOLDER_PATH, "*.parquet")), key = os.path.getctime)
        csvFiles = sorted(glob.glob(os.path.join(self.DATA_BACKUPS_FOLDER_PATH, "*.csv")), key = os.path.getctime)

        if min(len(parquetFiles), len(csvFiles)) > self.MAX_BACKUP_FILES_PER_FORMAT:
            parquetFilesToDelete = parquetFiles[:len(parquetFiles) - self.MAX_BACKUP_FILES_PER_FORMAT]
            csvFilesToDelete = csvFiles[:len(csvFiles) - self.MAX_BACKUP_FILES_PER_FORMAT]
            for i in range(min(len(parquetFilesToDelete), len(csvFilesToDelete))):
                try:
                    os.remove(parquetFilesToDelete[i])
                    os.remove(csvFilesToDelete[i])
                except Exception as e:
                    print(f"Error deleting file: {e}")