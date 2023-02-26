#proberen vanaf gewenste pagina vertrekken naar info pagina maar zonder succes 2U 20min

import requests
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
#driver.implicitly_wait(25)
driver.get(url)

#l = driver.find_element(By.CSS_SELECTOR, "button.button-primary")
#driver.execute_script("arguments[0].click()", l)

r = driver.find_element(By.CSS_SELECTOR, "div.button-wrapper a.hidden")
driver.execute_script("arguments[0].click()", r)