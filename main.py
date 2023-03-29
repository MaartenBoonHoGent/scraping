from ryanair import getDataRyanair
from transaviaApi import run as getDataTransavia
from tui import getFlightData as getDataTui
from brusselsAirlines import runBrusselsAirlines as getDataBrusselsAirlines
from databaseConnection import DataBaseConnection
import pandas as pd


def main(verbose=False):
    """
    Main function: it will call the functions to get the data from the different
    websites and save it to the database
    """

    database = DataBaseConnection()
    # Start with ryanair
    functions = [getDataRyanair, getDataTransavia, getDataTui, getDataBrusselsAirlines]
    generalisationFunctions = [None, None, None, None]
    names = ["Ryanair", "Transavia", "Tui", "Brussels Airlines"]

    for dataFunction, generalisationFunction, name in zip(functions, generalisationFunctions, names):
        if verbose:
            print(f"Getting data from {name}")
        data = dataFunction()
        data = generalisationFunction(data)
        # Save the data to the database
        database.writeDataFrame(data)
if __name__ == "__main__":
    main()
