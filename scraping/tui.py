import json
from datetime import date, timedelta
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from databaseConnection import DataBaseConnection
from log.logger import Logger

PATH = json.load(open("settings.json"))["chromedriver_path"]


def createUrl(flyingFrom,
              flyingTo,
              depDate,
              adults=1,
              children=0,
              childAge="",
              choiceSearch="true",
              searchType='pricegrid',
              nearByAirports="true",
              currency='EUR',
              isOneWay="true"):
    baseUrl = "http://www.tuifly.be/flight/nl/search?"
    baseUrl = f"{baseUrl}flyingFrom%5B%5D={flyingFrom}&flyingTo%5B%5D={flyingTo}&depDate={depDate}&adults={adults}" \
              f"&children={children}&childAge={childAge}&choiceSearch={choiceSearch}&searchType={searchType}" \
              f"&nearByAirports={nearByAirports}&currency={currency}&isOneWay={isOneWay}"
    return baseUrl


def object_to_dataframe(json_data):
    lijst = []
    date_data_recieved = datetime.now().date()
    ORIGINS = ['OST', 'ANR', 'BRU', 'LGG']
    for data in json_data['flightViewData']:
        productId = data['productId']
        totalPrice = data['totalPrice']
        # adultPrice = data['adultPrice']
        departDate = data['journeySummary']['departDate']
        arrivalDate = data['journeySummary']['arrivalDate']
        depTime = data['journeySummary']['depTime']
        arrivalTime = data['journeySummary']['arrivalTime']
        departAirportCode = data['journeySummary']['departAirportCode']
        arrivalAirportCode = data['journeySummary']['arrivalAirportCode']
        journeyType = data['journeySummary']['journeyType']
        journeyDuration = data['journeySummary']['journeyDuration']
        arrivalAirportName = data['journeySummary']['arrivalAirportName']
        departAirportName = data['journeySummary']['departAirportName']
        availableSeats = data['journeySummary']['availableSeats']
        carrierCode = data['journeySummary']['carrierCode']
        carrierName = data['journeySummary']['carrierName']
        totalNumberOfStops = len(data['flightsectors']) - 1
        flightNumber = data['flightsectors'][0]['flightNumber']

        if departAirportCode in ORIGINS and "2023-04-01" <= departDate <= "2023-10-01":
            lijst.append({'date_data_recieved': date_data_recieved, 'departDate': departDate,
                          'arrivalDate': arrivalDate, 'flightNumber': flightNumber, 'productId': productId,
                          'depTime': depTime, 'arrivalTime': arrivalTime, 'departAirportCode': departAirportCode,
                          'arrivalAirportCode': arrivalAirportCode, 'journeyType': journeyType,
                          'totalNumberOfStops': totalNumberOfStops, 'journeyDuration': journeyDuration,
                          'arrivalAirportName': arrivalAirportName, 'departAirportName': departAirportName,
                          'availableSeats': availableSeats,
                          'carrierCode': carrierCode, 'carrierName': carrierName, 'totalPrice': totalPrice,
                          })
    return pd.DataFrame(lijst)


def getFlightData():
    DESTINATION = [
        'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP',
        'PMI', 'TFS']
    ORIGINS = ['OST', 'ANR', 'BRU', 'LGG']
    if datetime.now().date() <= date(2021, 4, 1):
        dateIn = date(2023, 4, 1)
    else:
        dateIn = date(datetime.now().year, datetime.now().month,
                      datetime.now().day)
    dateOut = date(2023, 10, 1)
    retrieveData = []
    addDays = timedelta(days=7)
    amountOfDataToRetrieve = len(DESTINATION) * len(ORIGINS) * (int((dateOut - dateIn).days / 7) + 1)
    fullCounter = 0
    while dateIn <= dateOut:
        dateIn += addDays
        counter = 0
        for destination in DESTINATION:
            print(f"Retrieving data for {destination} on {dateIn.strftime('%Y-%m-%d')} ({counter}/{len(DESTINATION)}) "
                  f"({fullCounter}/{amountOfDataToRetrieve})")
            counter += 1
            fullCounter += 1
            try:
                url = "http://www.tuifly.be/flight/nl/"
                URL = createUrl(depDate=dateIn.strftime("%Y-%m-%d"),
                                flyingFrom='BRU',
                                flyingTo=destination)
                options = webdriver.ChromeOptions()
                driver_service = Service(executable_path=PATH)
                driver = webdriver.Chrome(service=driver_service, options=options)
                # options = webdriver.FirefoxOptions()
                # driver_service = Service(executable_path=PATH)
                # driver = webdriver.Firefox(service=driver_service, options=options)
                
                options.add_experimental_option("detach", True)
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                driver.maximize_window()
                driver.implicitly_wait(25)
                driver.get(url)
                driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()
                driver.get(URL)
                data = driver.execute_script(
                    "return JSON.stringify(searchResultsJson)")
                driver.close()

                json_object = json.loads(data)
                retrieveData.append(object_to_dataframe(json_object))
            except Exception as e:
                logger = Logger()
                logger.logError(e)
                continue

    retrieveData = pd.concat(retrieveData)
    return retrieveData


def main():
    retrieveData = getFlightData()
    result_Data = retrieveData.drop_duplicates()

    if result_Data.empty:
        return

    # Rename the columns

    result_Data = result_Data.rename(
        columns={
            "carrierName": "maatschappij_naam",
            "departAirportCode": "vertrek_airport_code",
            "departAirportName": "vertrek_luchthaven_naam",
            "arrivalAirportCode": "aankomst_airport_code",
            "arrivalAirportName": "aankomst_luchthaven_naam",
            "totalPrice": "prijs",
            "availableSeats": "vrije_plaatsen",
            "productId": "flightkey",
            "flightNumber": "vluchtnummer",
            "arrivalTime": "aankomst_tijdstip",
            "depTime": "vertrek_tijdstip",
            "totalNumberOfStops": "aantal_stops",
        }
    )

    result_Data["opgehaald_tijdstip"] = datetime.now()

    # Zip the flightkey 

    result_Data["flightkey"] = (result_Data["flightkey"].str[0:8] + "-" +
                                result_Data["flightkey"].str[8:16] + "-" +
                                result_Data["flightkey"].str[16:24] + "-" +
                                result_Data["flightkey"].str[24:32])
    # Remove all the columns that are not needed
    result_Data = result_Data[["maatschappij_naam", "vertrek_airport_code", "vertrek_luchthaven_naam",
                               "aankomst_airport_code", "aankomst_luchthaven_naam", "opgehaald_tijdstip",
                               "prijs", "vrije_plaatsen", "flightkey", "vluchtnummer", "aankomst_tijdstip",
                               "vertrek_tijdstip", "aantal_stops"]]

    # Open a connection to the database
    logger = Logger()
    logger.log(airline="TUI", amountOfRows=len(result_Data.index))

    database = DataBaseConnection()
    database.connect()
    database.writeDataFrame(result_Data)
    database.disconnect()


if __name__ == "__main__":
    main()
