# https://www.ryanair.com/gb/en

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

def createUrl(destination, origin, dateOut, dateIn, adt=1, chd=0, inf=0, teen=0, disc=0, promoCode="", includeConnectingFlights="false", flexDaysBeforeOut=2, flexDaysOut=2, flexDaysBeforeIn=2, flexDaysIn=2, roundTrip="true", toUs="AGREED"):
    baseUrl = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?"
    baseUrl = f"{baseUrl}ADT={adt}&CHD={chd}&DateIn={dateIn}&DateOut={dateOut}&Destination={destination}&Disc={disc}&INF={inf}&Origin={origin}&TEEN={teen}&promoCode={promoCode}&IncludeConnectingFlights={includeConnectingFlights}&FlexDaysBeforeOut={flexDaysBeforeOut}&FlexDaysOut={flexDaysOut}&FlexDaysBeforeIn={flexDaysBeforeIn}&FlexDaysIn={flexDaysIn}&RoundTrip={roundTrip}&ToUs={toUs}"
    return baseUrl

def json_to_dataframe(json_string):
    json_data = json.loads(json_string)    
    output_data = []
    for trip in json_data['trips']:
        for flight in trip['dates']:
            for flight_details in flight['flights']:
                flight_info = {}
                flight_info['origin'] = trip['origin']
                flight_info['originName'] = trip['originName']
                flight_info['destination'] = trip['destination']
                flight_info['destinationName'] = trip['destinationName']
                flight_info['routeGroup'] = trip['routeGroup']
                flight_info['tripType'] = trip['tripType']
                flight_info['upgradeType'] = trip['upgradeType']
                flight_info['dateOut'] = flight['dateOut']
                flight_info['flightNumber'] = flight_details['flightNumber']
                flight_info['faresLeft'] = flight_details['faresLeft']
                flight_info['infantsLeft'] = flight_details['infantsLeft']
                flight_info['fareClass'] = flight_details['regularFare']['fareClass']
                flight_info['amount'] = flight_details['regularFare']['fares'][0]['amount']
                output_data.append(flight_info)
    return pd.DataFrame(output_data)

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
retrievedData.to_csv("Ryanair.csv")