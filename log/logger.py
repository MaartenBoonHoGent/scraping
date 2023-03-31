

class Logger():
    def __init__():
        self._logFile = "log.csv"

    def log(airline: str, amountOfRows: int = None):
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