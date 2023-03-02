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

def typeText(driver, element, text):
    driver.execute_script("arguments[0].value = arguments[1];", element, text)
    

def createURL(origin, destination, date) -> str:
    # return "https://www.transavia.com/nl-BE/boek-een-vlucht/vluchten/zoeken/"
    return "https://www.transavia.com/nl-BE/home/"
    return "https://customerlogin.transavia.com/379fb04b-964b-4985-965c-2d9097eef215/b2c_1a_customer_signuporsignin/oauth2/v2.0/authorize?client_id=ed9a43b5-64fb-47b1-abac-bc510a1802e5&redirect_uri=https%3a%2f%2fwww.transavia.com%2fapi%2fpersonalaccountauth%2fcallback&response_mode=form_post&response_type=code&scope=openid&state=OpenIdConnect.AuthenticationProperties%3dSrosqYacI8Trp_1220lgIM3GzG1BagyAtTbkQiLx3Cw4Aaf_601hDC9rmRILezbqu6q0GQ3nKNCHATDD8q9bPy5JFQf1clrR6QMGYks8SFaRx0_5obJAGf0nUiT46VAZmRHTa7eDuOjuHik8JFrP-6jt8qPJJVerjoGsIGp9hZw90Hd0VkmpKyPRjxuhp516n0fbs7uowx3l1UsoSZ0pDBuSyBE0XdTjfHl8CT8Bbwb7KFf2HgQzLMwZEcjd_5vWM7XTVLetLkCNUJLMBGoewNi3fY1wiqCVz96_MraXEgv3I5xHzQBJWe1mvRN35qhH9Wwb4ot_sDpJN_h2uaAGgp6MpvnYhJfsLGn18ZNia1CqKiPmQn2aE7ZbC1FeS2HGAJE6Vk91gtm43V024cJ_g1GB6xiBUWRmCjyuT4WyOfMG1iG2VUQS1PcFzBjOGbxU0rxPHSTAVwMP-I5EO-1Agui541UqPIH3w9Cka6JFDE4&ui_locales=nl-BE&locale=nl-BE&x-client-SKU=ID_NET&x-client-ver=1.0.40306.1554"
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
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            for d in DATES:
                print(f"Getting data for {origin} to {destination} on {d}")
                # Get the data from the website
                url = createURL(origin, destination, d)
                # Open the selenium driver
                driver = createDriver(PATH)
                driver.get(url)
                # Wait for the page to load
                randomEvent(driver)
                # Find the element with following classes: rc-anchor-center-item rc-anchor-checkbox-label
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "recaptcha-anchor-label")))
                element = driver.find_element(By.ID, "recaptcha-anchor-label")
                driver.execute_script("arguments[0].click()", element)
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
    