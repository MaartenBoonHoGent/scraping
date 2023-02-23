# https://www.ryanair.com/gb/en

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

def createUrl(destination, origin, dateOut, dateIn, adt=1, chd=0, inf=0, teen=0, disc=0, promoCode="", includeConnectingFlights="false", flexDaysBeforeOut=2, flexDaysOut=2, flexDaysBeforeIn=2, flexDaysIn=2, roundTrip="true", toUs="AGREED"):
    baseUrl = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?"
    baseUrl = f"{baseUrl}ADT={adt}&CHD={chd}&DateIn={dateIn}&DateOut={dateOut}&Destination={destination}&Disc={disc}&INF={inf}&Origin={origin}&TEEN={teen}&promoCode={promoCode}&IncludeConnectingFlights={includeConnectingFlights}&FlexDaysBeforeOut={flexDaysBeforeOut}&FlexDaysOut={flexDaysOut}&FlexDaysBeforeIn={flexDaysBeforeIn}&FlexDaysIn={flexDaysIn}&RoundTrip={roundTrip}&ToUs={toUs}"
    return baseUrl


def json_to_dataframe(json_object):
    data = json.loads(json_object)
    trips = data['trips']
    dataframes = []
    for trip in trips:
        dates = trip['dates']
        for date in dates:
            flights = date['flights']
            for flight in flights:
                flight_data = {
                    'origin': trip['origin'],
                    'originName': trip['originName'],
                    'destination': trip['destination'],
                    'destinationName': trip['destinationName'],
                    'dateOut': date['dateOut'],
                    'flightNumber': flight['flightNumber'],
                    'duration': flight['duration'],
                    'faresLeft': flight['faresLeft'] if 'faresLeft' in flight else None,
                    'infantsLeft': flight['infantsLeft'] if 'infantsLeft' in flight else None,
                }
                if 'regularFare' in flight:
                    fares = flight['regularFare']['fares']
                    for fare in fares:
                        fare_data = flight_data.copy()
                        fare_data.update({
                            'fareType': fare['type'],
                            'fareAmount': fare['amount'],
                            'fareCount': fare['count'],
                            'fareHasDiscount': fare['hasDiscount'],
                            'farePublishedFare': fare['publishedFare'],
                            'fareDiscountInPercent': fare['discountInPercent'],
                            'fareHasPromoDiscount': fare['hasPromoDiscount'],
                            'fareDiscountAmount': fare['discountAmount'],
                            'fareHasBogof': fare['hasBogof'],
                        })
                        dataframes.append(pd.DataFrame(fare_data, index=[0]))
                else:
                    dataframes.append(pd.DataFrame(flight_data, index=[0]))
    
    return pd.concat(dataframes, ignore_index=True) if len(dataframes) > 0 else pd.DataFrame()


def getData():
    DESTINATIONS = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'PMI', 'TFS']
    ORIGINS = ['BRU', 'CRL']
    dateIn = "2023-04-01"
    dateOut = "2023-10-01"
    retrievedData = []
    
    amnt = len(DESTINATIONS) * len(ORIGINS)
    counter = 0
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            counter += 1
            print(f"Request {counter}/{amnt}", end="\r")
            URL = createUrl(dateIn=dateIn, dateOut=dateOut, destination=destination, origin=origin)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "lxml")
            result = soup.find("p").text
            json_object = json.loads(result)
            retrievedData.append(json_to_dataframe(json.dumps(json_object)))
    retrievedData = pd.concat(retrievedData)
    return retrievedData

retrievedData = getData()
print(retrievedData)
retrievedData.to_csv("Ryanair.csv")