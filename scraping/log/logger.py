import datetime
import os

import pandas as pd


class Logger:
    def __init__(self):
        self._logFile = "log.csv"
        self._errorLogFile = "errorLog.csv"

    @property
    def errors(self) -> pd.DataFrame:
        # Check if the log file exists
        if not os.path.exists(self._errorLogFile):
            # Create the log file
            return pd.DataFrame(columns=["timestamp", "error", "traceback"])

        else:
            # Read the log file
            return pd.read_csv(self._errorLogFile)

    @property
    def logs(self) -> pd.DataFrame:
        # Check if the log file exists
        if not os.path.exists(self._logFile):
            # Create the log file
            return pd.DataFrame(columns=["timestamp", "airline", "amountOfRows"])

        else:
            # Read the log file
            return pd.read_csv(self._logFile)

    def log(self, airline: str, amountOfRows: int = None):
        # Create a current timestamp
        timestamp = datetime.datetime.now().timestamp()

        # Create a new row
        newRow = pd.DataFrame([[timestamp, airline, amountOfRows]], columns=["timestamp", "airline", "amountOfRows"])

        # Check if the log file exists
        if not os.path.exists(self._logFile):
            # Create the log file
            newRow.to_csv(self._logFile, index=False)
        
        else:
            # Append the row to the log file
            newRow.to_csv(self._logFile, mode="a", header=False, index=False)

    def logError(self, error: Exception):
        # Create a current timestamp
        timestamp = datetime.datetime.now().timestamp()

        # Create a new row
        newRow = pd.DataFrame([[timestamp, error, error.__traceback__]], columns=["timestamp", "error", "traceback"])

        # Check if the log file exists
        if not os.path.exists(self._errorLogFile):
            # Create the log file
            newRow.to_csv(self._errorLogFile, index=False)

        else:
            # Append the row to the log file
            newRow.to_csv([[timestamp,self._errorLogFile]],columns=["timestamp","error"] mode="a", header=False, index=False)
