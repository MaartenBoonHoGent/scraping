from seleniumwire import webdriver

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

LANDEN = ["palermo-sicilie", "faro", "alicante", "malaga", "palma-de-mallorca", "tenerife", "Kerkyra", "brindisi", "ibiza"]
MAANDEN = ["", "", "", "APRIL", "MEI", "JUNI", "JULI", "AUGUSTUS", "SEPTEMBER", "OKTOBER"]
TEST= ["palermo-sicilie"]

def object_to_dataframe(json_data):
    lijst = []
    date_data_recieved = datetime.datetime.now().date()
    for data in json_data['data']['airBoundGroups']:
        arrivalAirportCode = data['boundDetails']['originLocationCode']
        departAirportCode = data['boundDetails']['destinationLocationCode']
        journeyDuration = data['boundDetails']['duration']
        totalNumberOfStops = len(data['boundDetails']['segments']) - 1

        if 'segments' in data['boundDetails']:
            for segment in data['boundDetails']['segments']:
                flightId = segment['flightId']
                if 'connectionTime' in segment:
                    connectionTime = segment['connectionTime']
                for flight in json_data['dictionaries']['flight'][flightId]:
                    depTime=flight['departure']['dateTime']
                    arrivalTime=flight['arrival']['dateTime']
        else:
            flightId = data['boundDetails']['flightId']
            for flight in json_data['dictionaries']['flight'][flightId]:
                    depTime = flight['departure']['dateTime']
                    arrivalTime = flight['arrival']['dateTime']

        for bounds in data['airBounds'][1]:
            availableSeats = bounds['availabilityDetails']['quota']
            basePrice = bounds['prices']['totalPrices']['base']
            totalPrice = bounds['prices']['totalPrices']['total']
            tax = bounds['prices']['totalPrices']['totalTaxes']
    

            lijst.append({ 'date_data_recieved': date_data_recieved, 'depTime': depTime, 'arrivalTime': arrivalTime, 
                          'arrivalAirportCode': arrivalAirportCode, 'departAirportCode': departAirportCode, 'journeyDuration': journeyDuration, 
                          'totalNumberOfStops': totalNumberOfStops, 'connectionTime':connectionTime,'flightId': flightId, 'availableSeats': availableSeats, 
                          'basePrice': basePrice, 'totalPrice': totalPrice, 'tax': tax

            })
    return pd.DataFrame(lijst)

def getData():
    # Create the driver
    driver = createDriver()
    print(f"Driver created | {str(datetime.datetime.now())}")
    # Go to the website
    for bestemming in TEST:
        # in geval van fouten opnieuw beginnen
        opnieuw = True
        #dit is om te zeggen welke datum je moet starten om te kiezen
        if(date.today().month  < 4):
            selecteerStartDag = 1
            selecteerStartMaand = 3
        else:
            selecteerStartDag = date.today().day
            selecteerStartMaand = date.today().month - 1

        url = f"https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-{bestemming}"
        print(f"Bestemming {bestemming} | {str(datetime.datetime.now())}")
        while(opnieuw or (selecteerStartMaand !=4  and selecteerStartDag != 2)):
            driver.get(url)
            try:
                opnieuw = False
                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//*[@id='flightSearch']/div[1]/div/ul/li[1]/label")))

                #enkelle reizen aanklikken 
                label_click = driver.find_element(By.CSS_SELECTOR, "label.checkbox-like.lh.lh-checkmark-checked")
                driver.execute_script("arguments[0].click()", label_click)

                #openen van info
                openen = driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[1]/div/ul/li[1]/label")
                driver.execute_script("arguments[0].click()", openen)

                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[3]/span[1]")))

                #datum zetten
                open_dagen = driver.find_element(By.XPATH, "//*[@id='flightsTab']/div[4]/div[1]/div[1]/label")
                driver.execute_script("arguments[0].click()", open_dagen)
                #maand selecteren
                while(driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[3]/span[1]").text != '%s 2023' % MAANDEN[selecteerStartMaand]):
                    volgende = driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[2]")
                    driver.execute_script("arguments[0].click()", volgende)
                #dag selecteren
                tabel = driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[4]/table[1]")
                dagen = tabel.find_elements(By.CSS_SELECTOR, "tr.date-row td")

                #beginnen van loop
                for d in dagen:
                    retrievedData = []
                    if(d.text == str(selecteerStartDag)):
                        selecteerStartDag += 1
                    
                        #dag aanklikken
                        driver.execute_script("arguments[0].click()", d)
                        
                        #klikken voor naar juiste pagina te gaan
                        r = driver.find_element(By.CSS_SELECTOR, "button#searchFlights") # Findbutton by CSS selector
                        driver.execute_script("arguments[0].click()", r)
                        
                        # wachten tot tijd geladen is
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[7]/div/div/footer/div[1]/lhg-upsell-back-button/button")))


                        # Getting the object
                        responseBody = None
                        print("dag:",str(selecteerStartDag) , " maand:" , str(selecteerStartMaand), "dest:" , bestemming)
                              
                        for request in driver.requests:
                            if request.response:
                                if 'air-bounds' in request.url.lower():
                                    responseBody = io.BytesIO(request.response.body)
                                    break

                        # Decompress the gzipped content
                        with gzip.GzipFile(fileobj=responseBody) as f:
                            content = f.read()

                        content = json.loads(content.decode('utf-8'))
                        content = object_to_dataframe(content)
                        print(content)
                        content.to_csv("BruAir.csv", mode=('a' if os.path.exists("BruAir.csv") else "w"), header=(not os.path.exists("BruAir.csv")), index=False)
            except Exception as e:
                print(traceback.format_exc())
                exit(0)
                opnieuw = True
                driver.get(url) 
    retrievedData = pd.concat(content)
    return retrievedData
                        
            #na elke dag krijgen we een except
            #en zo resetten we
            

def main():
    retrievedData = getData()
    result_Data = retrievedData.drop_duplicates()
    result_Data.to_csv("BruAir.csv", index=False)

if __name__ == "__main__":
    main()
    