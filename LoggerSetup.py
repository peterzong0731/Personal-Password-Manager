import datetime
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

class LoggerSetupClass:
    @staticmethod
    def setupLogger():
        if getattr(sys, 'frozen', False):
            logDirectory = os.path.join(sys.executable, "Logs")
        else:
            logDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
        os.makedirs(logDirectory, exist_ok=True)

        currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
        logFile = os.path.join(logDirectory, f"PasswordManager_{currentDate}.log")
        handler = TimedRotatingFileHandler(logFile, when="D", interval=1, backupCount=5, encoding="utf-8")

        # Force rotation if needed
        LoggerSetupClass.forceRotation(handler, logFile)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s]: %(message)s",
            handlers=[handler],
        )

        sys.excepthook = LoggerSetupClass.logUncaughtExceptions

    @staticmethod
    def forceRotation(handler, logFile):
        if os.path.exists(logFile):
            oldCreatedDate = datetime.datetime.fromtimestamp(os.path.getctime(logFile)).date()
            currentDate = datetime.datetime.now().date()

            if oldCreatedDate < currentDate:
                handler.doRollover()

    @staticmethod
    def logUncaughtExceptions(excType, excValue, excTraceback):
        """Log any uncaught exception that would crash the program."""
        logger = logging.getLogger()
        if issubclass(excType, KeyboardInterrupt): # Allow Ctrl+C to work normally
            sys.__excepthook__(excType, excValue, excTraceback)
            return

        logger.critical("Unhandled Exception", exc_info=(excType, excValue, excTraceback))
