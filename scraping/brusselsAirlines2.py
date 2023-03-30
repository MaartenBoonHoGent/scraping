from seleniumwire import webdriver



def createDriver():
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--disable-dev-shm-usage')
    webdriver_options.add_argument('--disable-extensions')
    webdriver_options.add_argument('--disable-dev-shm-usage')

    driver_service = Service(executable_path=PATH)

    driver = webdriver.Chrome(service=driver_service, options=webdriver_options)

def main():
    # Create the driver