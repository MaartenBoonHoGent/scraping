import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random
# Get the places where the plane is flying to
# DESTINATIONS = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'PMI', 'TFS']
DESTINATIONS = ['HER']
ORIGINS = ['BRU']
# dates = pd.date_range("2023-04-01", "2023-10-01", freq="D")
dates = pd.date_range("2023-04-01", "2023-04-01", freq="D")
DATES = dates.strftime("%Y-%m-%d").tolist()
PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

# LOGIN
MAIL = "wasomi3092@wireps.com"
PASSWORD = "^Ph!gRA46jSPSt"

GMAIL = "transaviabot@gmail.com"

def typeText(driver, element, text):
    driver.execute_script("arguments[0].value = arguments[1];", element, text)
    

def createURL(origin, destination, date) -> str:
    # return "https://www.transavia.com/nl-BE/boek-een-vlucht/vluchten/zoeken/"
    return "https://www.transavia.com/nl-BE/home/"
def createDriver(path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--ignore-certificate-errors')
    driver_service = Service(executable_path=path)
    driver = webdriver.Chrome(service=driver_service,options=options)
    driver.maximize_window()
    return driver

def randomEvent(driver):
    # Random event: Get a random number between 1 and 2
    randomN = random.randint(1, 2)
    # If the random number is 1, then click on the "I agree" button
    if randomN == 1:
        # Time.sleep for random amount of time
        n = random.randint(1, 10)
        time.sleep(n)
        print(f"Random event: sleeping for {n} seconds")

    elif randomN == 2:
        # Resize the window
        driver.set_window_size(random.randint(800, 1000), random.randint(800, 1000))
        print(f"Random event: resizing the window")
        randomEvent(driver)

def getData():
    # Log in to gmail 
    
    driver = createDriver(PATH)

    loginSite = "https://accounts.google.com/"
    driver.get(loginSite)
    # Wait for the page to load
    eMailElement = driver.find_element(By.ID, "identifierId")
    driver.execute_script("arguments[0].value = arguments[1];", eMailElement, GMAIL)
    # Click on the next button
    nextBtt = driver.find_element(By.ID, "identifierNext")
    driver.execute_script("arguments[0].click()", nextBtt)
    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd")))
    # Enter the password
    passwordElement = driver.find_element(By.NAME, "Passwd")
    driver.execute_script("arguments[0].value = arguments[1];", passwordElement, PASSWORD)
    # Click on the next button
    nextBtt = driver.find_element(By.ID, "passwordNext")
    driver.execute_script("arguments[0].click()", nextBtt)
    randomEvent(driver)
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            for d in DATES:
                print(f"Getting data for {origin} to {destination} on {d}")
                # Get the data from the website
                url = createURL(origin, destination, d)
                # Open the selenium driver
                driver.get(url)
                # Wait for the page to load
                randomEvent(driver)
                # ToDo: ByPass the captcha
                # For now: Manually solve the captcha
                time.sleep(20)
                
                """WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signInName")))
                # Login
                randomEvent(driver)
                # Click the saveCookie button: class -> cb__button-text
                saveCookie = driver.find_element(By.CSS_SELECTOR, "span.cb__button-text")
                driver.execute_script("arguments[0].click()", saveCookie) 
                # Get the signInName element
                signInName = driver.find_element(By.ID, "signInName")
                randomEvent(driver)
                # Get the password element
                password = driver.find_element(By.ID, "password")
                # Get the next button
                randomEvent(driver)
                nextButton = driver.find_element(By.ID, "next")
                # Random event
                randomEvent(driver)
                # Type the text
                typeText(driver, signInName, MAIL)
                typeText(driver, password, PASSWORD)
                # Click the next button
                driver.execute_script("arguments[0].click()", nextButton) """
if __name__ == "__main__":
    getData()
    