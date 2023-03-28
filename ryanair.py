    # https://www.ryanair.com/gb/en

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

def createUrl(destination, origin, dateOut, dateIn, adt=1, chd=0, inf=0, teen=0, disc=0, promoCode="", includeConnectingFlights="false", flexDaysBeforeOut=2, flexDaysOut=2, flexDaysBeforeIn=2, flexDaysIn=2, roundTrip="true", toUs="AGREED"):
    baseUrl = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?"
    baseUrl = f"{baseUrl}ADT={adt}&CHD={chd}&DateIn={dateIn}&DateOut={dateOut}&Destination={destination}&Disc={disc}&INF={inf}&Origin={origin}&TEEN={teen}&promoCode={promoCode}&IncludeConnectingFlights={includeConnectingFlights}&FlexDaysBeforeOut={flexDaysBeforeOut}&FlexDaysOut={flexDaysOut}&FlexDaysBeforeIn={flexDaysBeforeIn}&FlexDaysIn={flexDaysIn}&RoundTrip={roundTrip}&ToUs={toUs}"
    return baseUrl

def object_to_dataframe(json_data):
    output_data = []
    #termsOfUse = json_data['termsOfUse']
    currency = json_data['currency']
    currPrecision = json_data['currPrecision']
    # tripType = trip['tripType']
    # upgradeType = trip['upgradeType']
    serverTimeUTC = datetime.now().date()
    for trip in json_data['trips']:
        origin = trip['origin']
        originName = trip['originName']
        destination = trip['destination']
        destinationName = trip['destinationName']
        routeGroup = trip['routeGroup']
        tripType = trip['tripType']
        upgradeType = trip['upgradeType']
        for dat in trip['dates']:
            dateOut = dat['dateOut'].split("T")[0]
            flights = dat['flights']
            for flight in flights:
                faresLeft = flight['faresLeft']
                flightKey = flight['flightKey']
                infantLeft = flight['infantLeft'] if 'infantLeft' in flight else None
                operatedBy = flight['operatedBy']
                flightNumber = flight['flightNumber']
                duration = flight['duration']
                #timeUTCStart = flight['timeUTC'][0].split("T")[0]
                #timeUTCEnd = flight['timeUTC'][1].split("T")[0]
                timeStart = flight['time'][0].split("T")[0]
                timeEnd = flight['time'][1].split("T")[0]
                depTime=flight['time'][0].split("T")[1].split(".")[0]
                arrivalTime = flight['time'][1].split("T")[1].split(".")[0]
                segmentAmnt = len(flight['segments'])
                if not "regularFare" in flight:
                    continue
                fares = flight["regularFare"]['fares'] if 'fares' in flight["regularFare"] else None
                #fareKey = flight["regularFare"]['fareKey']
                fareClass = flight["regularFare"]['fareClass']
                for fare in fares:
                    fareType = fare['type']
                    fareAmount = fare['amount']
                    fareCount = fare['count']
                    fareHasDiscount = fare['hasDiscount']
                    farePublishedFare = fare['publishedFare']
                    fareDiscountInPercent = fare['discountInPercent']
                    fareHasPromoDiscount = fare['hasPromoDiscount']
                    fareDiscountAmount = fare['discountAmount']
                    fareHasBogof = fare['hasBogof']

                    if dateOut >= "2023-04-01" and dateOut <= "2023-10-01": 
                        output_data.append({
                            #"termsOfUse": termsOfUse,
                            "dateDataRecieved": serverTimeUTC,
                            "departAirportCode": origin,
                            "departAirportName": originName,
                            "arrivalAirportCode": destination,
                            "arrivalAirportName": destinationName,
                            "departDate": timeStart,
                            "arrivalDate": timeEnd,
                            "depTime":depTime,
                            "arrivalTime" : arrivalTime,
                            "journeyDuration": duration,
                            "flightNumber": flightNumber,
                            "routeGroup": routeGroup,
                            "JourneyType": tripType,
                            #"upgradeType": upgradeType,
                            "availableSeats": faresLeft,
                            #"infantLeft": infantLeft,
                            #"operatedBy": operatedBy,
                            #"timeUTCStart": timeUTCStart,
                            #"timeUTCEnd": timeUTCEnd,
                            "totalNumberOfStops": segmentAmnt,
                            #"fareType": fareType,
                            #"fareKey": fareKey,
                            #"fareClass": fareClass,
                            "totalPrice": fareAmount,
                            "currency": currency,
                            #"currPrecision": currPrecision,
                            "fareCount": fareCount,
                           # "fareHasDiscount": fareHasDiscount,
                            "farePublishedFare": farePublishedFare,
                            #"fareDiscountInPercent": fareDiscountInPercent,
                            #"fareHasPromoDiscount": fareHasPromoDiscount,
                            #"fareDiscountAmount": fareDiscountAmount,
                            #"fareHasBogof": fareHasBogof,
                            "flightKey":flightKey
                        })
    return pd.DataFrame(output_data)

def getData():
    DESTINATIONS = ['CFU', 'HER', 
                    'RHO', 'BDS', 
                    'NAP', 'PMO', 
                    'FAO', 'ALC',
                    'IBZ', 'AGP', 
                    'PMI', 'TFS']
    ORIGINS = ['BRU', 'CRL']
    retrievedData = []
    dates = pd.date_range("2023-04-01", "2023-04-01", freq="D")
    # dates = pd.date_range("2023-04-01", "2023-04-01", freq="D")
    dates = dates.strftime("%Y-%m-%d").tolist()
    amnt = len(DESTINATIONS) * len(ORIGINS) * len(dates)
    counter = 0
    for dateOut in dates:
        for origin in ORIGINS:
            for destination in DESTINATIONS:
                counter += 1
                #print(f"Request {counter}/{amnt}", end="\r")
                print(f'Request {counter:2}/{amnt} {origin:3} - {destination:5} | {dateOut}', end='\r')
                URL = createUrl(dateIn="", dateOut=dateOut, destination=destination, origin=origin)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "lxml")
                result = soup.find("p").text
                json_object = json.loads(result)
                retrievedData.append(object_to_dataframe(json_object))
    retrievedData = pd.concat(retrievedData)
    return retrievedData

def main():
    retrievedData = getData()
    result_Data = retrievedData.drop_duplicates()            
    result_Data.to_csv("scraping/ryanair.csv", index=False)
if __name__ == "__main__":
    main()
