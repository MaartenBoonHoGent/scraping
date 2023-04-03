
import mysql.connector
import os
import datetime
import pandas as pd
from numpy import datetime64

import json

class DataBaseConnection:
    def __init__(self) -> None:

        # Print current working directory
        print("Current working directory: " + os.getcwd())
        inlogData = json.load(open("database/mysql_inlog.json"))

        self._connection = None
        self._username = inlogData["username"]
        self._password = inlogData["password"]
        self._databaseName = "dep_database"
        self._hostName = "127.0.0.1"
        self._buildFile = "../database/build.sql"



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

        if self._password == "":
            os.popen("mysql -u " + self._username + " " + self._databaseName + " < " + self._buildFile)
        else:
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
            "vertrek_airport_code": str,
            "vertrek_luchthaven_naam": str,
            "aankomst_airport_code": str,
            "aankomst_luchthaven_naam": str,
            "opgehaald_tijdstip": datetime64,
            "prijs": float,
            "vrije_plaatsen": int,
            "flightkey": str,
            "vluchtnummer": str,
            "aankomst_tijdstip": datetime64,
            "vertrek_tijdstip": datetime64,
            "aantal_stops": int,
        }

    

        for column in requiredColumns:
            # Check if the column is present
            assert column in dataframe.columns, "Column " + column + " is not present in the dataframe"
            # Check if the column is of the correct type
            # Try to convert the column to the correct type
            try:
                dataframe[column] = dataframe[column].astype(requiredColumns[column])
            except:
                # If the conversion fails, raise an error
                assert dataframe[column].dtype == requiredColumns[column], f"Column {column} is not of the correct type. Expected {requiredColumns[column]}, got {dataframe[column].dtype}"
        
        dataframe = dataframe[
            ["maatschappij_naam", "vertrek_airport_code", "vertrek_luchthaven_naam",
            "aankomst_airport_code", "aankomst_luchthaven_naam", "opgehaald_tijdstip",
            "prijs", "vrije_plaatsen", "flightkey", "vluchtnummer", "aankomst_tijdstip",
            "vertrek_tijdstip", "aantal_stops"]
        ]
        # Insert the dataframe into the database using stored procedure 'insert_record'
        cursor = self._connection.cursor()
        for index, row in dataframe.iterrows():
            cursor.callproc("insert_record", [
                row["maatschappij_naam"],
                row["vertrek_airport_code"],
                row["vertrek_luchthaven_naam"],
                row["aankomst_airport_code"],
                row["aankomst_luchthaven_naam"],
                row["opgehaald_tijdstip"],
                row["prijs"],
                row["vrije_plaatsen"],
                row["flightkey"],
                row["vluchtnummer"],
                row["aankomst_tijdstip"],
                row["vertrek_tijdstip"],
                row["aantal_stops"],
            ])

        cursor.close()
        self._connection.commit()
