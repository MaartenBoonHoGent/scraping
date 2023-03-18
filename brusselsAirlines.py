#KIJKEN VOOR CODE ALS ER GEEN VLUCHTEN ZIJN
# geenVluchten = True
# try:
#   span = driver.find_element(By.CSS_SELECTOR, "div.text span")
#   print(span.text)
# except:
#   geenVluchten = False
from datetime import date
import time


from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from concurrent.futures import ThreadPoolExecutor




#empty final df
dfinal= pd.DataFrame({})

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
#"Kerkyra", "brindisi", "ibiza"

landen = ["palermo-sicilie", "faro", "alicante", "malaga", "palma-de-mallorca", "tenerife"]

#opzetten parralel werken
def set_up_threads(landen):
  with ThreadPoolExecutor(max_workers=1) as executor:
    return executor.map(get_landen,landen)


def get_landen(bestemming):
  # in geval van fouten opnieuw beginnen
  opnieuw = True
  while(opnieuw):
    try:
      opnieuw = False
      options = webdriver.ChromeOptions()
      options.add_experimental_option("detach", True)
      options.add_experimental_option("excludeSwitches", ["enable-automation"])
      options.add_experimental_option('useAutomationExtension', False)
      driver_service = Service(executable_path=PATH)
      driver = webdriver.Chrome(service=driver_service,options=options)

      stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
  
      url = f"https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-{bestemming}"
      driver.get(url)
      
      #enkelle reizen aanklikken 
      label_click = driver.find_element(By.CSS_SELECTOR, "label.checkbox-like.lh.lh-checkmark-checked")
      driver.execute_script("arguments[0].click()", label_click) # Click the button
      #klikken voor naar juiste pagina te gaan
      r = driver.find_element(By.CSS_SELECTOR, "button#searchFlights") # Findbutton by CSS selector
      driver.execute_script("arguments[0].click()", r)


      # wachten tot tijd geladen is
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[3]/refx-page-title-pres/div/div/refx-page-title-box-pres/h1/div[2]")))
      time.sleep(10)

      #DATA OPHALEN
      #start & stop locatie 
      locaties = driver.find_element(By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[3]/refx-page-title-pres/div/div/refx-page-title-box-pres/h1/div[2]")
      start, stop = locaties.text.split(" naar ")
      

      #info per reis
      reizen = driver.find_elements(By.CSS_SELECTOR, "body app refx-app-layout div div.main-content.justify-content-center refx-upsell refx-basic-in-flow-layout div div.content-wrapper div:nth-child(3) div div div refx-upsell-premium-cont refx-upsell-premium-pres mat-accordion refx-upsell-premium-row-pres")
      for r in reizen:
          #tijden voor starten en stoppen      
          startUur = r.find_element(By.CSS_SELECTOR, "div.bound-departure-datetime").text
          aankomstUur = r.find_element(By.CSS_SELECTOR, "div.bound-arrival-datetime").text

          #duur
          duur = r.find_element(By.CSS_SELECTOR, "span.duration-value").text

          #Economy Classic nemen voor prijs en stoelen
          try:
              button = r.find_element(By.CSS_SELECTOR, "button.mat-focus-indicator.mat-button.mat-button-base.flight-card-button.ng-star-inserted")
              driver.execute_script("arguments[0].click()", button)
              time.sleep(2)
              economie = r.find_element(By.CSS_SELECTOR, "mat-expansion-panel.mat-expansion-panel")
              economie_blokken = economie.find_elements(By.CSS_SELECTOR, "li.fare-card-list-item.ng-star-inserted")
          except:
            prijs = -1; stoelen = -1 #geen prijsen dus ook geen stoelen (vlucht boeken via bellen)
          #prijs
          try:
            for e in economie_blokken:
              if(e.find_element(By.CSS_SELECTOR, "div.refx-body-2.price-card-title-label").text == "Economy Classic"):
                ec = e
                prijs = e.find_element(By.CSS_SELECTOR, "span.price-amount").text
                break
          except:
            prijs = -1; stoelen = -1 #geen vluchten voor economy classic
          #stoelen
          try:
            stoel = ec.find_element(By.CSS_SELECTOR, "span.refx-caption.message-value").text
            stoel2 = stoel.split(" ")
            stoelen = stoel2[1]
          except:
            stoelen = -1


          # #stop namen van vliegvelden
          # tussenStops = r.find_elements(By.CSS_SELECTOR, "div.detailsSecondLine span.ng-star-inserted")
          # tussenStops.pop()
          # setStops= set()
          # for x in tussenStops:
          #     van, naar= x.text.split(" - ")
          #     setStops.add(van)
          #     setStops.add(naar)
          # setStops.remove("BRU")

          #stops: dit zijn niet alleen maar vliegvelden maar ook stations/ deze zien we niet in de stoppen
          try:
            Aantalstops = r.find_element(By.CSS_SELECTOR, "div.bound-nb-stop span").text
          except:
            Aantalstops = 0



          # gedetailleerdeknop= r.find_element(By.CSS_SELECTOR,"div.d-flex.refx-caption.ng-star-inserted")
          # driver.execute_script("arguments[0].click()", gedetailleerdeknop)


          # tussenStops = driver.find_elements(By.CSS_SELECTOR, "bdo.airport-code")
          # Flightcodes = driver.find_elements(By.CSS_SELECTOR,"span.seg-marketing-flight-number.ng-star-inserted")
          # planecodes = driver.find_elements(By.CSS_SELECTOR,"span.seg-operating-aircraft")
          # setStops= set()
          # for x in tussenStops:
          #     setStops.add(x)
          # setStops.remove('(BRU)')

          # setFlightcodes=set()
          # for x in Flightcodes:
          #    setFlightcodes.add(x)

          # setplanecodes = set()
          # for x in planecodes:
          #    setplanecodes.add(x)

          # print(setStops)
          # print(setFlightcodes)
          # print(setplanecodes)


          # #Flightnummers
          # Flightnummers = r.find_elements(By.CSS_SELECTOR, "div.availInfoAirlineContainer div.flightNumber")
          # setNummers= set()
          # for x in Flightnummers:
          #   setNummers.add(x.text)

          # #uitvoerders vluchten
          # Uitvoerders = r.find_elements(By.CSS_SELECTOR, "div.availInfoAirlineContainer div.airlineName")
          # setUitvoerders= set()
          # for x in Uitvoerders :
          #   setUitvoerders.add(x.text)

          # print("\ndatum:", date.today(),  "   start:", start, "   stop:", stop, "\nVertrek uur:", startUur, "  Aankomst uur:", aankomstUur, " duur:", duur.text, "\nprijs:", prijsresult, " stoelen:", stoelenresult, "\nstops:", stopresult, " tussenstop Vliegvelden:", setStops, " FlightNummers:", setNummers, " Uitvoerders:", setUitvoerders)


          # #add data to datafram
          # df = pd.DataFrame({
          #   'datum': [date.today()],
          #   'start': [start],
          #   'stop': [stop],
          #   'Vertrek uur':[startUur],
          #   'Aankomst uur':[aankomstUur],
          #   'duur':[duur.text],
          #   'prijs':[prijsresult],
          #   'stoelen':[stoelenresult],
          #   'stops':[stopresult],
          #   'tussenstop Viegvelden':[setStops],
          #   'FlightNummers':[setNummers],
          #   'Uitvoerders':[setUitvoerders]
          # })
          # #voeg dataframes samen
          # dfinal = pd.concat([dfinal,df],ignore_index = True)

          print("start:", start, "   stop:", stop, " duur:", duur, " \nstartUur:", startUur, " aankomstUur:", aankomstUur, " AantalStops:", Aantalstops, "\nprijs:", prijs, " stoelen:", stoelen)
      driver.quit()
            
    except:
      opnieuw = True
      driver.quit()


dfinal.to_csv('scraping/brusselsAirlines.csv', index=False)

if __name__ == "__main__":
    # read and generate urls
    set_up_threads(landen)
