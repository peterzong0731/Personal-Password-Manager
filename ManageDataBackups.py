import datetime
import functools
import glob
import logging
import os
import pandas as pd
import sys

def log_function_call(func):
    """Decorator to log function calls with arguments and return values."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"[Manage Backups Thread] - Calling: {func.__name__}()")
        logging.debug(f"[Manage Backups Thread] - Calling: {func.__name__}() | Args: {args} | Kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

def log_all_methods(cls):
    """Class decorator to log all method calls."""
    for attr_name, attr in cls.__dict__.items():
        if callable(attr) and not attr_name.startswith("__"):
            setattr(cls, attr_name, log_function_call(attr))
    return cls

@log_all_methods
class ManageDataBackupsClass():
    # Global constants
    LOGGER = logging.getLogger()
    MAX_BACKUP_FILES_PER_FORMAT = 10
    if getattr(sys, 'frozen', False): #Running as an executable
        DATA_BACKUPS_FOLDER_PATH = os.path.join(sys.executable, "Data_Backups")
    else: # Running as a script
        DATA_BACKUPS_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data_Backups")

    # Global dynamic variables
    login_data = pd.DataFrame()

    def __init__(self, loginData: pd.DataFrame):
        self.LOGGER.info("[Manage Backups Thread] : Manage backups thread started")
        os.makedirs(self.DATA_BACKUPS_FOLDER_PATH, exist_ok=True)
        self.login_data = loginData
        self.SaveBackup()
        self.CleanupBackupsFolder()

    def SaveBackup(self):
        currentDateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csvBackupPath = os.path.join(self.DATA_BACKUPS_FOLDER_PATH, f"Login_Data_Backup_{currentDateTime}.csv")
        parquetBackupPath = os.path.join(self.DATA_BACKUPS_FOLDER_PATH, f"Login_Data_Backup_{currentDateTime}.parquet")

        self.login_data.to_csv(csvBackupPath, index = False)
        self.LOGGER.info('[Manage Backups Thread] : CSV backup file saved: "%s"', csvBackupPath)
        self.login_data.to_parquet(parquetBackupPath, index = False)
        self.LOGGER.info('[Manage Backups Thread] : Parquet backup file saved: "%s"', parquetBackupPath)

    def CleanupBackupsFolder(self):
        csvFiles = sorted(glob.glob(os.path.join(self.DATA_BACKUPS_FOLDER_PATH, "*.csv")), key = os.path.getctime)
        parquetFiles = sorted(glob.glob(os.path.join(self.DATA_BACKUPS_FOLDER_PATH, "*.parquet")), key = os.path.getctime)

        if min(len(csvFiles), len(parquetFiles)) > self.MAX_BACKUP_FILES_PER_FORMAT:
            csvFilesToDelete = csvFiles[:len(csvFiles) - self.MAX_BACKUP_FILES_PER_FORMAT]
            parquetFilesToDelete = parquetFiles[:len(parquetFiles) - self.MAX_BACKUP_FILES_PER_FORMAT]
            for i in range(min(len(csvFilesToDelete), len(parquetFilesToDelete))):
                try:
                    os.remove(csvFilesToDelete[i])
                    self.LOGGER.info('[Manage Backups Thread] : CSV backup file deleted: "%s"', csvFilesToDelete[i])
                    os.remove(parquetFilesToDelete[i])
                    self.LOGGER.info('[Manage Backups Thread] : Parquet backup file deleted: "%s"', parquetFilesToDelete[i])                    
                except Exception as e:
                    self.LOGGER.error('[Manage Backups Thread] : Exception deleting file:', exc_info=True)