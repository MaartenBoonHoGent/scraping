import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# Get the places where the plane is flying to
# DESTINATIONS = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'PMI', 'TFS']
DESTINATIONS = ['HER']
ORIGINS = ['BRU']
# dates = pd.date_range("2023-04-01", "2023-10-01", freq="D")
dates = pd.date_range("2023-04-01", "2023-04-01", freq="D")
DATES = dates.strftime("%Y-%m-%d").tolist()
PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

def createURL(origin, destination, date) -> str:
    return "https://www.transavia.com/nl-BE/boek-een-vlucht/vluchten/zoeken/"

def createDriver(path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--ignore-certificate-errors')
    driver_service = Service(executable_path=path)
    driver = webdriver.Chrome(service=driver_service,options=options)
    driver.maximize_window()
    return driver

def getData():
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            for d in DATES:
                print(f"Getting data for {origin} to {destination} on {d}")
                # Get the data from the website
                url = createURL(origin, destination, d)
                print(url)
                # Open the selenium driver
                driver = createDriver(PATH)
                driver.get(url)
                # Wait for the page to load
                time.sleep(.5)
if __name__ == "__main__":
    getData()
    