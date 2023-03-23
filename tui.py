from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta
import re
import pandas as pd
# from webdriver_manager.chrome import ChromeDriverManager
import json


PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

# url = "http://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=OST&flyingTo%5B%5D=HER&depDate=2023-05-05&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"



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
    baseUrl = f"{baseUrl}flyingFrom%5B%5D={flyingFrom}&flyingTo%5B%5D={flyingTo}&depDate={depDate}&adults={adults}&children={children}&childAge={childAge}&choiceSearch={choiceSearch}&searchType={searchType}&nearByAirports={nearByAirports}&currency={currency}&isOneWay={isOneWay}"
    return baseUrl


def object_to_dataframe(json_data):
    lijst = []
    date_data_recieved = datetime.now().date()
    ORIGINS = ['OST', 'ANR', 'BRU', 'LGG']
    for data in json_data['flightViewData']:
        productId = data['productId']
        totalPrice = data['totalPrice']
        adultPrice = data['adultPrice']
        departDate = data['journeySummary']['departDate']
        arrivalDate = data['journeySummary']['arrivalDate']
        depTime = data['journeySummary']['depTime']
        arrivalTime= data['journeySummary']['arrivalTime']
        departAirportCode = data['journeySummary']['departAirportCode']
        arrivalAirportCode = data['journeySummary']['arrivalAirportCode']
        journeyType = data['journeySummary']['journeyType']
        journeyDuration = data['journeySummary']['journeyDuration']
        arrivalAirportName = data['journeySummary']['arrivalAirportName']
        departAirportName = data['journeySummary']['departAirportName']
        availableSeats = data['journeySummary']['availableSeats']
        carrierCode = data['journeySummary']['carrierCode']
        carrierName = data['journeySummary']['carrierName']
        totalNumberOfStops = len(data['flightsectors']) -1
        flightNumber = data['flightsectors'][0]['flightNumber']


        if departAirportCode in ORIGINS and departDate >= "2023-04-01" and departDate <= "2023-10-01": 
            lijst.append({'date_data_recieved': date_data_recieved, 'departDate': departDate, 'arrivalDate': arrivalDate, 'flightNumber': flightNumber,'productId': productId,
                          'depTime': depTime, 'arrivalTime': arrivalTime, 'departAirportCode': departAirportCode, 
                          'arrivalAirportCode': arrivalAirportCode, 'journeyType': journeyType,'totalNumberOfStops':totalNumberOfStops,'journeyDuration': journeyDuration, 
                          'arrivalAirportName': arrivalAirportName, 'departAirportName': departAirportName, 'availableSeats': availableSeats, 
                          'carrierCode': carrierCode, 'carrierName': carrierName, 'totalPrice': totalPrice, 'adultPrice': adultPrice
                      }) 
    return pd.DataFrame(lijst)


def getFlightData():
    DESTINATION = [
        'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP',
        'PMI', 'TFS']
    ORIGINS = ['OST', 'ANR', 'BRU', 'LGG']
    dateIn = date(2023, 4, 1)
    dateOut = date(2023, 10, 1)
    retrieveData = []
    addDays = timedelta(days=7)
    options = webdriver.ChromeOptions()
    driver_service = Service(executable_path=PATH)
    driver = webdriver.Chrome(service=driver_service,options=options)
    while dateIn <= dateOut:
        dateIn += addDays
        counter = 0
        for destination in DESTINATION :
            counter += 1
            url = "http://www.tuifly.be/flight/nl/"
            URL = createUrl(depDate=dateIn.strftime("%Y-%m-%d"),
                            flyingFrom='BRU',
                            flyingTo=destination)
            
            options.add_experimental_option("detach", True)
            options.add_argument('--ignore-certificate-errors')
            driver.maximize_window()
            driver.implicitly_wait(25)
            driver.get(url)
            driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()
            driver.get(URL)
            data = driver.execute_script("return JSON.stringify(searchResultsJson)")
            driver.close()

            json_object = json.loads(data)                
            retrieveData.append(object_to_dataframe(json_object))
    retrieveData = pd.concat(retrieveData)
    return retrieveData


def main():
    retrieveData = getFlightData()
    result_Data = retrieveData.drop_duplicates()            
    result_Data.to_csv("scraping/tuifly2.csv", index=False)
if __name__ == "__main__":
    main()
