from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "https://quotes.toscrape.com/js/"

options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service,options=options)
# driver.maximize_window()
driver.implicitly_wait(25)
driver.get(url)

quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote span.text")
for q in quotes:
    print(q.text)


