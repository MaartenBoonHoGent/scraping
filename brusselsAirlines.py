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
r = driver.find_element(By.CSS_SELECTOR, "div.bp-mock p a.button")
driver.execute_script("arguments[0].click()", r)


#wachten tot pagina laad
time.sleep(40)

#DIT WERKT NOG NIET
#klikken op de "enkele reis" knop en opnieuw laden
#pelle testing things
#l = driver.find_element(By.CSS_SELECTOR, "input.0")
#l = driver.find_element_by_name("tripType")
#l =driver.find_element(By.CLASS_NAME("input O ng-untouched ng-pristine ng-valid"));

l = driver.find_element(By.XPATH(".//label[@class='label ng-star-inserted']/input[1][@class='input O ng-untouched ng-pristine ng-valid']"))

#"input O ng-untouched ng-pristine ng-valid" 
if(l): print("gelukt")
#driver.execute_script("arguments[0].click()", l)

