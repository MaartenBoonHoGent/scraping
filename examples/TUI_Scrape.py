from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager 
import json

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "http://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=OST&flyingTo%5B%5D=HER&depDate=2023-05-05&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service,options=options)
driver.maximize_window()
driver.implicitly_wait(25)
driver.get(url)

driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()


element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
    ) 

# selection = driver.find_element(By.CSS_SELECTOR, "div#page div.container footer script")
result = element.get_attribute('innerHTML')

print(result)
