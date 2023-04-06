from seleniumwire import webdriver
from databaseConnection import DataBaseConnection
from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import date
import time
import datetime
import re
import gzip
import io
import urllib.request
import json
import pandas as pd
import os
import traceback

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"


def createDriver():
    driver_service = Service(executable_path=PATH)
    driver = webdriver.Chrome(service=driver_service)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


LANDEN = ["palermo-sicilie", "faro", "alicante", "malaga",
          "palma-de-mallorca", "tenerife", "Kerkyra", "brindisi", "ibiza"]
MAANDEN = ["", "", "", "APRIL", "MEI", "JUNI",
           "JULI", "AUGUSTUS", "SEPTEMBER", "OKTOBER"]

def object_to_dataframe(json_data):
    lijst = []
    date_data_recieved = datetime.datetime.now().date()
    for data in json_data['data']['airBoundGroups']:
        flightId = []
        depDate = []
        arrivalDate = []
        counter = 0
        arrivalAirportCode = data['boundDetails']['originLocationCode']
        departAirportCode = data['boundDetails']['destinationLocationCode']
        journeyDuration = data['boundDetails']['duration']
        totalNumberOfStops = len(data['boundDetails']['segments']) - 1

        for airbounds in data['airBounds']:
            if counter == 1:
                for details in airbounds['availabilityDetails']:
                    flightId.append(details['flightId'])
                    availableSeats = details['quota']
                basePrice = airbounds['prices']['unitPrices'][0]['prices'][0]['base']
                totalPrice = airbounds['prices']['unitPrices'][0]['prices'][0]['total']
                tax = airbounds['prices']['unitPrices'][0]['prices'][0]['totalTaxes']
            counter += 1

        if 'segments' in data['boundDetails']:
            for segment in data['boundDetails']['segments']:
                if 'connectionTime' in segment:
                    connectionTime = segment['connectionTime']
        else:
            flightId = data['boundDetails']['flightId']

        temp =  flightId[0].split('-')
        depDate = f'%s-%s-%s' % (temp[3], temp[4], temp[5])
        temp =  flightId[len(flightId) - 1].split('-')
        arrivalDate = f'%s-%s-%s' % (temp[3], temp[4], temp[5])

        lijst.append({'date_data_recieved': date_data_recieved,
                      'arrivalAirportCode': arrivalAirportCode, 'departAirportCode': departAirportCode, 'journeyDuration': journeyDuration,
                      'totalNumberOfStops': totalNumberOfStops, 'connectionTime': connectionTime, 'availableSeats': availableSeats,
                      'basePrice': basePrice, 'totalPrice': totalPrice, 'tax': tax, 'flightId': flightId, 'depDate': depDate, 'arrivalDate': arrivalDate,

                      })
    return pd.DataFrame(lijst)


def getData():
    dataVoorDatabase = []
    # Create the driver
    driver = createDriver()
    print(f"Driver created | {str(datetime.datetime.now())}")
    # Go to the website
    for bestemming in LANDEN:
        # dit is om te zeggen welke datum je moet starten om te kiezen
        if (date.today().month < 4):
            selecteerStartDag = 1
            selecteerStartMaand = 3
        else:
            selecteerStartDag = date.today().day
            selecteerStartMaand = date.today().month - 1

        url = f"https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-{bestemming}"
        print(f"Bestemming {bestemming} | {str(datetime.datetime.now())}")
        while ((selecteerStartMaand != 10)):
            driver.get(url)
            try:
                WebDriverWait(driver, 120).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='flightSearch']/div[1]/div/ul/li[1]/label")))

                # enkelle reizen aanklikken
                label_click = driver.find_element(
                    By.CSS_SELECTOR, "label.checkbox-like.lh.lh-checkmark-checked")
                driver.execute_script("arguments[0].click()", label_click)

                # openen van info
                openen = driver.find_element(
                    By.XPATH, "//*[@id='flightSearch']/div[1]/div/ul/li[1]/label")
                driver.execute_script("arguments[0].click()", openen)

                WebDriverWait(driver, 120).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[3]/span[1]")))

                # datum zetten
                open_dagen = driver.find_element(
                    By.XPATH, "//*[@id='flightsTab']/div[4]/div[1]/div[1]/label")
                driver.execute_script("arguments[0].click()", open_dagen)
                # maand selecteren
                while (driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[3]/span[1]").text != '%s 2023' % MAANDEN[selecteerStartMaand]):
                    volgende = driver.find_element(
                        By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[2]")
                    driver.execute_script("arguments[0].click()", volgende)
                # dag selecteren
                tabel = driver.find_element(
                    By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[4]/table[1]")
                dagen = tabel.find_elements(By.CSS_SELECTOR, "tr.date-row td")

                # zoeken naar dag
                vorigeDag = selecteerStartDag
                for d in dagen:
                    retrievedData = []
                    if (d.text == str(selecteerStartDag)):
                        selecteerStartDag += 1

                        # dag aanklikken
                        driver.execute_script("arguments[0].click()", d)
                        break
                # als de dag niet gevonden is, dan naar volgende maand gaan
                if selecteerStartDag == vorigeDag:
                    selecteerStartMaand += 1
                    selecteerStartDag = 1
                else:
                    # klikken voor naar juiste pagina te gaan
                    # Findbutton by CSS selector
                    r = driver.find_element(
                        By.CSS_SELECTOR, "button#searchFlights")
                    driver.execute_script("arguments[0].click()", r)

                    # wachten tot tijd geladen is
                    try:
                        data = True
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                            (By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[7]/div/div/footer/div[1]/lhg-upsell-back-button/button")))
                    except:
                        data = False
                    
                    if(data):
                        # Getting the object
                        responseBody = None
                        
                        for request in driver.requests:
                            if request.response:
                                if 'air-bounds' in request.url.lower():
                                    responseBody = io.BytesIO(
                                        request.response.body)
                                    
                                    # Decompress the gzipped content
                                    with gzip.GzipFile(fileobj=responseBody) as f:
                                        content = f.read()

                                    content = json.loads(content.decode('utf-8'))
                                    content = object_to_dataframe(content)
                                    print(content)
                                    content.to_csv("BruAir.csv", mode=('a' if os.path.exists(
                                        "BruAir.csv") else "w"), header=(not os.path.exists("BruAir.csv")), index=False)
                                    dataVoorDatabase.append(content)
                                    break
                    
            except Exception as e:
                print(traceback.format_exc())
                exit(0)

    try:
        retrievedData = pd.concat(dataVoorDatabase)
    except Exception as e:
        retrievedData = None
        print(e)
    return retrievedData


def main():
    retrievedData = getData()
    
    # Get the data to be the right dataframe
    retrievedData["maatschappij_naam"] = "Brussels Airlines"
    retrievedData["vertrek_airport_code"] = retrievedData["departAirportCode"]
    retrievedData["vertrek_luchthaven_naam"] = None
    retrievedData["aankomst_airport_code"] = retrievedData["arrivalAirportCode"]
    retrievedData["aankomst_luchthaven_naam"] = None
    retrievedData["opgehaald_tijdstip"] = retrievedData["date_data_recieved"]
    retrievedData["prijs"] = retrievedData["totalPrice"]
    retrievedData["vrije_plaatsen"] = retrievedData["availableSeats"]
    retrievedData["flightkey"] = retrievedData["flightId"]
    retrievedData["vluchtnummer"] = None
    retrievedData["aankomst_tijdstip"] = retrievedData["arrivalDate"]
    retrievedData["vertrek_tijdstip"] = retrievedData["depDate"]
    retrievedData["aantal_stops"] = retrievedData["totalNumberOfStops"]

    # Remove all the columns that are not needed
    result_Data = retrievedData[
        ["maatschappij_naam", "vertrek_airport_code", "vertrek_luchthaven_naam",
         "aankomst_airport_code", "aankomst_luchthaven_naam", "opgehaald_tijdstip",
         "prijs", "vrije_plaatsen", "flightkey", "vluchtnummer", "aankomst_tijdstip",
         "vertrek_tijdstip", "aantal_stops"]
    ]

    # Open a connection to the database
    database = DataBaseConnection()
    database.connect()
    database.writeDataFrame(result_Data)
    database.disconnect()

    print("Done")


if __name__ == "__main__":
    main()
