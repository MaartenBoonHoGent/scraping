import http.client, urllib.request, urllib.parse, urllib.error, base64
import datetime
import time
import os
import pandas as pd
import json
from typing import List

APIKEY = '17c5625ff4424000b95a0ae6f3a23586'
FILE = './data/transaviaApi.csv'

headers = {'apikey': APIKEY}
renames = {
    'outboundFlight.id': 'outboundFlightId',
    'outboundFlight.departureDateTime': 'DepartureDateTime',
    'outboundFlight.arrivalDateTime': 'ArrivalDateTime',
    'outboundFlight.marketingAirline.companyShortName': 'Airline',
    'outboundFlight.flightNumber': 'FlightNumber',
    'outboundFlight.departureAirport.locationCode': 'DepartureAirport',
    'outboundFlight.arrivalAirport.locationCode': 'ArrivalAirport',
    'pricingInfoSum.totalPriceAllPassengers': 'TotalPriceAllPassengers',
    'pricingInfoSum.totalPriceOnePassenger': 'TotalPriceOnePassenger',
    'pricingInfoSum.baseFare': 'BaseFare',
    'pricingInfoSum.taxSurcharge': 'TaxSurcharge',
    'pricingInfoSum.currencyCode': 'CurrencyCode',
    'pricingInfoSum.productClass': 'ProductClass',
    'deeplink.href': 'Deeplink',
    'resultSet': 'ResultSet'
}

def params(origin: str, destination: str, date: List[datetime.datetime]) -> str:
    # Create the dates string
    if len(date) == 1:
        date = date[0].strftime('%Y%m%d')
    else:
        startDate = date[0].strftime('%Y%m%d')
        endDate = date[1].strftime('%Y%m%d')
        date = startDate + '-' + endDate
    return urllib.parse.urlencode({ 'origin': origin, 'destination': destination, 'originDepartureDate': date })

def request(params: str, headers: dict) -> str:
    for _ in range(10):
        try: 
            conn = http.client.HTTPSConnection('api.transavia.com')
            conn.request("GET", "/v1/flightoffers/?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            # Convert the bytes to a dictionary if it's not empty
            if data:
                data = data.decode('utf-8')
                data = json.loads(data)
            else:
                data = {}
            conn.close()
            return data
        except Exception as e:
            time.sleep(10)

def convertToDataFrame(data: dict) -> pd.DataFrame:
    if data:
        # Get the data from the dictionary
        df = pd.json_normalize(data, record_path=['flightOffer'], meta=['resultSet'])
        # ToDo: Normalize the data
        # Rename the columns
        df.rename(columns=renames, inplace=True)
        return df
    return None
def run():
    
    DESTINATIONS = [
        ['CFU', 'Corfu'],
        ['HER', 'Heraklion'],
        ['RHO', 'Rhodos'],
        ['BDS', 'Bari'],
        ['NAP', 'Napels'],
        ['PMO', 'Palermo'],
        ['FAO', 'Faro'],
        ['ALC', 'Alicante'],
        ['IBZ', 'Ibiza'],
        ['AGP', 'Malaga'],
        ['PMI', 'Palma de Mallorca'],
        ['TFS', 'Tenerife'],
    ]
    ORIGINS = [['BRU', "Brussel"]]
    # Create the dates
    dates = pd.date_range("2023-04-01", "2023-10-01", freq="D")
    # Convert to a list of datetime objects
    dates = dates.to_pydatetime().tolist()
    # Select with an interval of 30 days
    dates = dates[::30]

    # Remove the csv file if it exists
    if os.path.exists(FILE):
        os.remove(FILE)

    amount = len(ORIGINS) * len(DESTINATIONS) * (len(dates) - 1)
    counter = 1
    for originCode, originName in ORIGINS:
        for destinationCode, destinationName in DESTINATIONS:
            prevDate = dates[0]
            for date in dates[1:]:
                print(f'Request {counter:2}/{amount} {originName:10} - {destinationName:20} | {prevDate.strftime("%Y-%m-%d")} - {date.strftime("%Y-%m-%d")}', end='\r')
                counter += 1
                data = request(params(originCode, destinationCode, [prevDate, date]), headers)
                # Convert the data to a dataframe
                data = convertToDataFrame(data)
                # Add the data to the csv file
                if data is not None:
                    data.to_csv(FILE, mode='a', header=not os.path.exists(FILE), index=False)
                prevDate = date

if __name__ == '__main__':
    run()