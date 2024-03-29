import datetime
import os
import traceback

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
        timestamp = datetime.datetime.now().utcnow().isoformat()

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
        timestamp = datetime.datetime.utcnow().isoformat()

        # Convert traceback to string
        errorTraceback = "".join(traceback.format_tb(error.__traceback__))

        # Create a new row
        newRow = pd.DataFrame([[timestamp, str(error), errorTraceback]], columns=["timestamp", "error", "traceback"])

        # Check if the log file exists
        if not os.path.exists(self._errorLogFile):
            # Create the log file
            newRow.to_csv(self._errorLogFile, index=False)

        else:
            # Append the row to the log file
            newRow.to_csv(self._errorLogFile, mode="a", header=False, index=False)
