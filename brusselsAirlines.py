import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


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
time.sleep(25)


#data ophalen
#start
locaties = driver.find_element(By.CSS_SELECTOR, "span.bound")
start, stop = locaties.text.split(" - ")

#info per reis
reizen = driver.find_elements(By.CSS_SELECTOR, "cont-avail.ng-tns-c78-1")
for r in reizen:
    #tijden splitsen in 2 voor begin en eind
    tijden = r.find_element(By.CSS_SELECTOR, "span.time")
    startUur, aankomstUur = tijden.text.split(" - ")

    #duur
    duur = r.find_element(By.CSS_SELECTOR, "span.duration")

    #prijs
    prijs = r.find_element(By.CSS_SELECTOR, "label.cabinPrice")
    prijs2 = prijs.text.split(" ")
    prijsresult = prijs2[1] + " " + prijs2[2]

    #stoelen zorgen dat dit enkel van economie is
    stoelen = r.find_element(By.CSS_SELECTOR, "div.seats")
    stoelen2 = stoelen.text.split(" ")
    stoelenresult = stoelen2[0]

    #stop namen van vliegvelden
    tussenStops = r.find_elements(By.CSS_SELECTOR, "div.detailsSecondLine span.ng-star-inserted")
    tussenStops.pop()
    setStops= set()
    for x in tussenStops:
        van, naar= x.text.split(" - ")
        setStops.add(van)
        setStops.add(naar)
    setStops.remove("BRU")

    #stops: dit zijn niet alleen maar vliegvelden maar ook stations/ deze zien we niet in de stoppen
    stops = r.find_element(By.CSS_SELECTOR, "span.nbStops")
    stops2 = stops.text.split(" ")
    stopresult = stops2[0]

    print("\nstart:", start, "   stop:", stop, " tussenstop Vliegvelden:", setStops, "\nVertrek uur:", startUur, "  Aankomst uur:", aankomstUur, " duur:", duur.text, "\nprijs:", prijsresult, " stoelen:", stoelenresult, " stops:", stopresult)