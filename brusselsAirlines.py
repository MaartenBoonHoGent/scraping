#proberen vanaf gewenste pagina vertrekken naar info pagina maar zonder succes 2U 20min

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-malaga"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service,options=options)
driver.get(url)

#klikken voor naar juiste pagina te gaan
r = driver.find_element(By.CSS_SELECTOR, "button#searchFlights") # Findbutton by CSS selector
# LAbel has the following class: checkbox-like lh lh-checkmark-checked

label_click = driver.find_element(By.CSS_SELECTOR, "label.checkbox-like.lh.lh-checkmark-checked")
print(label_click)
driver.execute_script("arguments[0].click()", label_click) # Click the button
driver.execute_script("arguments[0].click()", r)


#wachten tot pagina geladen is
# s = driver.getCurrentUrl()
# while(not s.equals(url)):
#     #wachten tot pagina laad
#     time.sleep(1)
time.sleep(60)


#data ophalen
reizen = driver.find_elements(By.CSS_SELECTOR, "cont-avail.ng-tns-c78-1")
tel = 0
for r in reizen:
    tijden = r.find_element(By.CSS_SELECTOR, "span.time")
    print(tijden.text)