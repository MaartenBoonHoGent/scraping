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
import datetime
import time
import random
import re
# Get the places where the plane is flying to
# DESTINATIONS = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'PMI', 'TFS']
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
now = datetime.datetime.now()
date = datetime.datetime(2023, 10, 1)
MONTHS =    (date.year - now.year) * 12 + date.month - now.month
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
        print(f"Waiting {n} seconds {' ' * 20}", end="\r")
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
wait(1)
# Switch to the iframe
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[0])
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[0])
wait(1)
# Click on the button
anchor = driver.find_element(By.CSS_SELECTOR, "label#recaptcha-anchor-label")
anchor.click()
wait(2)
# Switch back to the main window
driver.switch_to.default_content()
# Go to the new frame
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[0])
driver.switch_to.frame(driver.find_elements(By.CSS_SELECTOR, "iframe")[-1])
buster = driver.find_elements(By.CSS_SELECTOR, ".button-holder.help-button-holder")[0]
buster.click()

# Wait for the buster to solve the captcha
wait(30)

# Switch back to the main window
driver.switch_to.default_content()

# Go to the actual link

driver.get('https://www.transavia.com/nl-BE/boek-een-vlucht/uitgebreid-zoeken/zoeken/')

wait(2)
# Select the origin
# Click on the div with class selectfield-wrapper HV-gw-delete-row--bp0 AS-counties-and-cities-form-field_field-container

results = {
    "originCode": [],
    "origin": [],
    "destinationCode": [],
    "destination": [],
    "price": [],
    "day": [],
    "month": [],
    "timeStart": [],
    "timeEnd": [],
    "dateRecorded": [],
}

for origin in ORIGINS:
    for destination in DESTINATIONS:
        originWrapper = driver.find_element(By.CSS_SELECTOR, "div.selectfield-wrapper.HV-gw-delete-row--bp0.AS-counties-and-cities-form-field_field-container")
        originWrapper.click()

        # Select the origin
        resultsWrapper = originWrapper.find_element(By.CSS_SELECTOR, "ol.results")
        # Select the option that has the value of the origin
        # Loop the options
        for option in resultsWrapper.find_elements(By.CSS_SELECTOR, "li"):
            # Get the text of the option
            text = option.text
            # If the text is equal to the origin, then click on the option
            if text.lower().strip().find(origin[1].lower()) != -1:
                driver.execute_script("arguments[0].click();", option)
                break

        # selectfield-wrapper HV-gw-delete-row--bp0 AS-counties-and-cities-form-field_field-container
        destinationWrapper = driver.find_elements(By.CSS_SELECTOR, "div.selectfield-wrapper.HV-gw-delete-row--bp0.AS-counties-and-cities-form-field_field-container")[1]
        destinationWrapper.click()

        resultsWrapper = destinationWrapper.find_element(By.CSS_SELECTOR, "ol.results")
        # Select the option that has the value of the destination
        # Loop the options
        for option in resultsWrapper.find_elements(By.CSS_SELECTOR, "li"):
            # Get the text of the option
            text = option.text
            # If the text is equal to the destination, then click on the option
            if text.lower().strip().find(destination[1].lower()) != -1:
                driver.execute_script("arguments[0].click();", option)
                break

        # Calculate the amount of months between now and 01-10-2023
        # Get the current date
        # Select the element with the text "Weet je al wanneer je wilt vertrekken?"
        titleElement = driver.find_elements(By.CSS_SELECTOR, "h3.h5")
        for element in titleElement:
            text = element.text
            if text.lower().strip().find("weet je al wanneer je wilt vertrekken?") != -1:
                driver.execute_script("arguments[0].click();", element)
                break        
        for i in range(0, MONTHS):

            wait(1)
            driver.find_element(By.XPATH, '//*[@id="alternativesearch"]/div[4]/div[2]/div/div/div[1]/div/div/div/div[2]/div').click()
            driver.find_element(By.XPATH, '//*[@id="data-flight-type"]/option[2]').click()

            wait(1)
            # Select the right month
            driver.find_element(By.XPATH, '//*[@id="alternativesearch"]/div[4]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]').click()
            wait(1)
            driver.find_element(By.XPATH, f'//*[@id="timeFrameSelection_SingleFlight_SpecificMonth"]/option[{i+1}]').click()
            wait(1)
            # Select the search button
            driver.find_element(By.XPATH, '//*[@id="alternativesearch"]/div[6]/div[2]/button').click()
            wait(1)

            # Check if there are flights available by checking if the button with class button-open AS-destination_toggle-button exists
            try:
                # If the button exists, then click on it
                button = driver.find_element(By.CSS_SELECTOR, "button.button-open.AS-destination_toggle-button")
                button.click()
            except:
                # If the button doesn't exist, then continue
                continue
            
            # Wait for the flights to load
            wait(2)
            # Get the table with the flights    
            table = driver.find_element(By.CSS_SELECTOR, 'ol.bulletless.AS-time-frame-list')
            # Get all the list elements for 
            for list_element in table.find_elements(By.CSS_SELECTOR, 'li.AS-time-frame-list_item.toggle-container-level-2.is-closed'):
                # Click on the list element
                split_text = list_element.text
                day = re.findall(r'\b\d{1,2}\b', split_text)[0]
                month = re.findall(r'\b[a-zA-Z]+\b', split_text)[1]
                price = re.findall(r'€\d+', split_text)[0]
                # Click on the toggle div
                toggle = list_element.find_element(By.CSS_SELECTOR, 'div.toggle-button-level-2')
                driver.execute_script("arguments[0].click();", toggle)
                wait(1)
                toggleContent = list_element.find_element(By.CSS_SELECTOR, 'div.toggle-content-level-2')
                split_text = toggleContent.text
                hours = re.findall(r'\d{2}:\d{2}', split_text)
                start_hour, end_hour = hours[0], hours[1]

                results["originCode"].append(origin[0])
                results["origin"].append(origin[1])
                results["destinationCode"].append(destination[0])
                results["destination"].append(destination[1])
                results["price"].append(price)
                results["day"].append(day)
                results["month"].append(month)
                results["timeStart"].append(start_hour)
                results["timeEnd"].append(end_hour)
                results["dateRecorded"].append(now.strftime("%d-%m-%Y %H:%M:%S"))

        
            df = pd.DataFrame.from_dict(results)
            df.to_csv("transavia.csv", index=False)
            df.to_csv("./scraping/transavia.csv", index=False)        
        
        # Refresh the page
        driver.refresh()