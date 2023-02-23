# https://www.ryanair.com/gb/en

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
    termsOfUse = json_data['termsOfUse']
    currency = json_data['currency']
    currPrecision = json_data['currPrecision']
    # tripType = trip['tripType']
    # upgradeType = trip['upgradeType']
    serverTimeUTC = json_data['serverTimeUTC']
    for trip in json_data['trips']:
        origin = trip['origin']
        originName = trip['originName']
        destination = trip['destination']
        destinationName = trip['destinationName']
        routeGroup = trip['routeGroup']
        tripType = trip['tripType']
        upgradeType = trip['upgradeType']
        for dat in trip['dates']:
            dateOut = dat['dateOut']
            flights = dat['flights']
            for flight in flights:
                faresLeft = flight['faresLeft']
                flightKey = flight['flightKey']
                infantLeft = flight['infantLeft'] if 'infantLeft' in flight else None
                operatedBy = flight['operatedBy']
                flightNumber = flight['flightNumber']
                duration = flight['duration']
                timeUTCStart = flight['timeUTC'][0]
                timeUTCEnd = flight['timeUTC'][1]
                timeStart = flight['time'][0]
                timeEnd = flight['time'][1]
                segmentAmnt = len(flight['segments'])
                fares = flight["regularFare"]['fares'] if 'fares' in flight["regularFare"] else None
                fareKey = flight["regularFare"]['fareKey']
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
                    output_data.append({
                        "termsOfUse": termsOfUse,
                        "currency": currency,
                        "currPrecision": currPrecision,
                        "serverTimeUTC": serverTimeUTC,
                        "origin": origin,
                        "originName": originName,
                        "destination": destination,
                        "destinationName": destinationName,
                        "routeGroup": routeGroup,
                        "tripType": tripType,
                        "upgradeType": upgradeType,
                        "dateOut": dateOut,
                        "faresLeft": faresLeft,
                        "flightKey": flightKey,
                        "infantLeft": infantLeft,
                        "operatedBy": operatedBy,
                        "flightNumber": flightNumber,
                        "duration": duration,
                        "timeUTCStart": timeUTCStart,
                        "timeUTCEnd": timeUTCEnd,
                        "timeStart": timeStart,
                        "timeEnd": timeEnd,
                        "segmentAmnt": segmentAmnt,
                        "fareType": fareType,
                        "fareKey": fareKey,
                        "fareClass": fareClass,
                        "fareAmount": fareAmount,
                        "fareCount": fareCount,
                        "fareHasDiscount": fareHasDiscount,
                        "farePublishedFare": farePublishedFare,
                        "fareDiscountInPercent": fareDiscountInPercent,
                        "fareHasPromoDiscount": fareHasPromoDiscount,
                        "fareDiscountAmount": fareDiscountAmount,
                        "fareHasBogof": fareHasBogof
                    })
    return pd.DataFrame(output_data)

def getData():
    DESTINATIONS = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'PMI', 'TFS']
    ORIGINS = ['BRU', 'CRL']
    retrievedData = []
    dates = pd.date_range("2023-04-01", "2023-10-01", freq="D")
    # dates = pd.date_range("2023-04-01", "2023-04-01", freq="D")
    dates = dates.strftime("%Y-%m-%d").tolist()
    amnt = len(DESTINATIONS) * len(ORIGINS) * len(dates)
    counter = 0
    for dateOut in dates:
        for origin in ORIGINS:
            for destination in DESTINATIONS:
                counter += 1
                print(f"Request {counter}/{amnt}", end="\r")
                URL = createUrl(dateIn="", dateOut=dateOut, destination=destination, origin=origin)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "lxml")
                result = soup.find("p").text
                json_object = json.loads(result)
                retrievedData.append(object_to_dataframe(json_object))
    retrievedData = pd.concat(retrievedData)
    return retrievedData

retrievedData = getData()
retrievedData.to_csv("scraping/ryanair.csv", index=False)