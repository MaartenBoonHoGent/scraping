import pandas as pd
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
# Get the places where the plane is flying to
# DESTINATIONS = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'PMI', 'TFS']
DESTINATIONS = ['HER']
ORIGINS = ['BRU']
# dates = pd.date_range("2023-04-01", "2023-10-01", freq="D")
dates = pd.date_range("2023-04-01", "2023-04-01", freq="D")
DATES = dates.strftime("%Y-%m-%d").tolist()
PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
HOMEPAGE = "https://www.transavia.com/nl-BE/home/"
# Get the data from the website

def createDriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # Log the current directory
    options.add_extension('./extensions/extension_2_0_1_0.crx')
    options.add_experimental_option("detach", True)
    options.add_argument('--ignore-certificate-errors')
    driver_service = Service(executable_path=PATH)
    driver = webdriver.Chrome(service=driver_service,options=options)
    return driver

def wait(n):
    while n > 0:
        print(f"Waiting {n} seconds", end="\r")
        time.sleep(1)
        n -= 1

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


# Open the website
driver = createDriver()
driver.get(HOMEPAGE)
# Use buster to solve the captcha
wait(10)
# Switch to the iframe
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[0])
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[0])
wait(5)
# Click on the button
anchor = driver.find_element(By.CSS_SELECTOR, "label#recaptcha-anchor-label")
anchor.click()
wait(5)
# Switch back to the main window
driver.switch_to.default_content()
# Go to the new frame
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[0])
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[-1])
buster = driver.find_elements(By.CSS_SELECTOR, ".button-holder.help-button-holder")[0]
buster.click()

# Wait for the buster to solve the captcha
wait(10)

# Switch back to the main window
driver.switch_to.default_content()
"""
backButton = driver.find_element(By.CSS_SELECTOR, "input#dateSelection_IsReturnFlight")
backButton.click()"""
# Go to the actual link

driver.get('https://www.transavia.com/nl-BE/boek-een-vlucht/uitgebreid-zoeken/zoeken/')

# driver.close()