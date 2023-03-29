import pandas as pd

"""
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
"""


def assertData (data: pd.DataFrame):
    assert data is not None, "The data is None"
    assert isinstance(data, pd.DataFrame), "The data is not a pandas DataFrame"


def generalizeTransavia(data: pd.DataFrame) -> pd.DataFrame:
    # TODO: generalize the transavia data
    # dateDataRecieved,departAirportCode,departAirportName,arrivalAirportCode,arrivalAirportName,departDate,arrivalDate,depTime,arrivalTime,journeyDuration,flightNumber,routeGroup,JourneyType,availableSeats,totalNumberOfStops,totalPrice,currency,fareCount,farePublishedFare,flightKey
    assertData(data)
    if data.empty:
        return pd.DataFrame(
            columns=[
                "maatschappij_naam",
                "vertrek_airport_code", #
                "vertrek_luchthaven_naam", #
                "aankomst_airport_code", #
                "aankomst_luchthaven_naam", #
                "opgehaald_tijdstip", #
                "prijs", #
                "vrije_plaatsen", #
                "flightkey",
                "vluchtnummer",
                "aankomst_tijdstip",
                "vertrek_tijdstip",
                "aantal_stops",
            ]
        )
    
    # Lowercase the column names
    data.columns = [x.lower() for x in data.columns]
    # Rename the columns
    """
    'outboundflightid', 'departuredatetime', 'arrivaldatetime', 'airline',
       'flightnumber', 'departureairport', 'arrivalairport',ingProject\scraping>'totalpriceallpassengers', 'totalpriceonepassenger', 'basefare',gineeringProject/scraping/test.py"
       'taxsurcharge', 'currencycode', 'productclass', 'deeplink',
       'resultset']
    """
    print(data.columns)
    print(data["airline"])
    data.rename(
        columns={
            "departuredatetime": "vertrek_tijdstip",
            "arrivaldatetime": "aankomst_tijdstip",
            "flightnumber": "vluchtnummer",
            "departureairport": "vertrek_airport_code",
            "arrivalairport": "aankomst_airport_code",
            "totalpriceonepassenger": "prijs",
        },
        inplace=True,
    )
    
    # Add the company name
    print(data)




def generalizeRyanair(data: pd.DataFrame):
    # TODO: generalize the ryanair data
    assertData(data)
    pass

def generalizeTui(data: pd.DataFrame):
    # TODO: generalize the tui data
    assertData(data)
    pass

def generalizeBrusselsAirlines(data: pd.DataFrame):
    # TODO: generalize the brussels airlines data
    assertData(data)
    pass
