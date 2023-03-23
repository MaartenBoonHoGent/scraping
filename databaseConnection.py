
import mysql.connector
import os
import datetime
import pandas as pd

class DataBaseConnection:
    def __init__(self) -> None:
        self._connection = None
        self._username = "FILLIN"
        self._password = 'FILLIN'
        self._databaseName = "dep_database"
        self._hostName = "127.0.0.1"
        self._buildFile = "database.sql"



    # Getters and setters
    @property
    def connection(self):
        return self._connection
    
    @property
    def hostName(self):
        return self._hostName

    def refresh(self):
        # -------------------------------#
        #   Refresh Database Connection #
        # -------------------------------#
        self.disconnect()
        self.connect()

    def connect(self):
        # -------------------------------#
        #   Connect to Database Server   #
        # -------------------------------#
        self._connection = mysql.connector.connect(
            user=self._username,
            password=self._password,
            # database=self._databaseName,
            host=self._hostName
        )
        # Check if the schema with databaseName exists
        cursor = self._connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + self._databaseName)
        cursor.close()
        self._connection.commit()
        # reopen the connection
        self._connection = mysql.connector.connect(
            user=self._username,
            password=self._password,
            database=self._databaseName,
            host=self._hostName
        )


    def open(self):
        # -------------------------------#
        #   Open Database Connection    #
        # -------------------------------#
        if self._connection is None:
            self.connect()

    def disconnect(self):
        # -------------------------------#
        #   Disconnect from Database     #
        # -------------------------------#
        self._connection.close()
        self._connection = None

    def delete(self):
        # Check if connection is open
        self.open()
        # Check if the schema with databaseName exists
        cursor = self._connection.cursor()

        # Completely delete the database, including all the tables, views, and stored procedures, and all data,
        # and all indexes, and all constraints
        cursor.execute("DROP DATABASE IF EXISTS " + self._databaseName)
        cursor.close()
        self._connection.commit()

    def build(self):
        # Check if connection is open
        self.open()
        # Get the dumpFile location
        cursor = self._connection.cursor()
        # Create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + self._databaseName)
        cursor.close()

        os.popen("mysql -u " + self._username + " -p" + self._password + " " + self._databaseName + " < " + self._buildFile)
        self.disconnect()
        self.connect()

    def writeDataFrame(self, dataframe: pd.DataFrame):
        # Check if connection is open
        self.open()

        assert isinstance(dataframe, pd.DataFrame)
        if dataframe.empty:
            return
        # assert the columns
        # Lowercase the column names
        dataframe.columns = [x.lower() for x in dataframe.columns]
        # Replace spaces with underscores
        dataframe.columns = [x.replace(" ", "_") for x in dataframe.columns]
        # Replace dashes with underscores
        dataframe.columns = [x.replace("-", "_") for x in dataframe.columns]
        # Replace dots with underscores
        dataframe.columns = [x.replace(".", "_") for x in dataframe.columns]
        # Replace slashes with underscores
        dataframe.columns = [x.replace("/", "_") for x in dataframe.columns]

        # Check if all the needed columns are present
        requiredColumns = {
            "maatschappij_naam": str,
            "maatschappij_code": str,
            "vertrek_airport_code": str,
            "vertrek_luchthaven_naam": str,
            "aankomst_airport_code": str,
            "aankomst_luchthaven_naam": str,
            "opgehaald_tijdstip": datetime.datetime,
            "prijs": float,
            "vrije_plaatsen": int,
            "flightkey": str,
            "vluchtnummer": str,
            "aankomst_tijdstip": datetime.datetime,
            "vertrek_tijdstip": datetime.datetime,
            "aantal_stops": int,
        }

        for column in requiredColumns:
            # Check if the column is present
            assert column in dataframe.columns, "Column " + column + " is not present in the dataframe"
            # Check if the column is of the correct type
            assert dataframe[column].dtype == requiredColumns[column], f"Column {column} is not of the correct type. Expected {requiredColumns[column]}, got {dataframe[column].dtype}"
        

        # start the transaction
        # TODO: Maatschappij 
        # Insert the maatschappij if needed, and get the id
        # This is done via a stored procedure called insertMaatschappij
        # The stored procedure returns the id of the maatschappij
        # The id is needed to insert the vlucht
        query = "CALL insertMaatschappij(%s, %s)"
        cursor = self._connection.cursor()
        cursor.executemany(query, dataframe[["maatschappij_naam", "maatschappij_code"]].values.tolist())
        self._connection.commit()
        cursor.close()
        
        # TODO: Luchthaven
        # TODO: Vlucht
        # TODO: Tijdgebaseerde data
