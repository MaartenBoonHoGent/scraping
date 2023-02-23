from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date,timedelta
import re
import pandas as pd 
# from webdriver_manager.chrome import ChromeDriverManager 
import json

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

#url = "http://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=OST&flyingTo%5B%5D=HER&depDate=2023-05-05&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"


def createUrl(flyingFrom, flyingTo, depDate, adults=1, children=0, childAge="", choiceSearch="true", searchType='pricegrid', nearByAirports="true", currency='EUR', isOneWay="true"):
    baseUrl = "http://www.tuifly.be/flight/nl/search?"
    baseUrl= f"{baseUrl}flyingFrom%5B%5D={flyingFrom}&flyingTo%5B%5D={flyingTo}&depDate={depDate}&adults={adults}&children={children}&childAge={childAge}&choiceSearch={choiceSearch}&searchType={searchType}&nearByAirports={nearByAirports}&currency={currency}&isOneWay={isOneWay}"
    return baseUrl


def getFlightData():
    DESTINATION = ['CFU']
    ORIGINS =['OST','ANR','BRU','LGG']
    dateIn = date(2023, 4, 1)
    dateOut = date(2023, 4, 1)
    retrieveData = []
    d = dateOut-dateIn


    amnt = len(DESTINATION) * len(ORIGINS)
    counter = 0
    for i in range(d.days+1):
        day=dateIn+timedelta(days=i)
        for origin in ORIGINS:
            for destination in DESTINATION:
                counter += 1
                print(f"Date = {day} Request {counter}/{amnt}", end="\r")
                URL = createUrl(depDate=day, flyingFrom=origin, flyingTo=destination)
                
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)
                options.add_argument('--ignore-certificate-errors')
                driver_service = Service(executable_path=PATH)
                driver = webdriver.Chrome(service=driver_service,options=options)
                driver.maximize_window()
                driver.implicitly_wait(25)
                driver.get(URL)
                driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()

                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
                ) 
                # selection = driver.find_element(By.CSS_SELECTOR, "div#page div.container footer script")
                result = element.get_attribute('innerHTML')
                result= re.search(r'\((.*?)\)',result).group(1)
                print(result)
retrieveData = getFlightData()
print(retrieveData)
