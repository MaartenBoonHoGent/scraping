#KIJKEN VOOR CODE ALS ER GEEN VLUCHTEN ZIJN
# geenVluchten = True
# try:
#   span = driver.find_element(By.CSS_SELECTOR, "div.text span")
#   print(span.text)
# except:
#   geenVluchten = False
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

landen = ["palermo-sicilie", "faro", "alicante", "malaga", "palma-de-mallorca", "tenerife", "Kerkyra", "brindisi", "ibiza"]

#empty final df
dfinal= pd.DataFrame({})

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service,options=options)

for bestemming in landen:
  # in geval van fouten opnieuw beginnen
  opnieuw = True
  while(opnieuw):
    try:
      opnieuw = False
      url = f"https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-{bestemming}"
      driver.get(url)

      #klikken voor naar juiste pagina te gaan
      r = driver.find_element(By.CSS_SELECTOR, "button#searchFlights") # Findbutton by CSS selector
      # LAbel has the following class: checkbox-like lh lh-checkmark-checked

      #enkelle reizen aanklikken 
      label_click = driver.find_element(By.CSS_SELECTOR, "label.checkbox-like.lh.lh-checkmark-checked")
      print(label_click)
      driver.execute_script("arguments[0].click()", label_click) # Click the button
      driver.execute_script("arguments[0].click()", r)


      #wachten tot tijd geladen is
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "cont-avail.ng-tns-c78-1")))


      # #datum vertrek zetten
      # datum = driver.find_element(By.CSS_SELECTOR, "pres-datepicker-v2 div.container label.label ")
      # datum.send_keys("01.04.2023")
      # volgende = driver.find_element(By.CSS_SELECTOR, "button.newSearchButton")
      # driver.execute_script("arguments[0].click()", volgende)



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

          #juiste groep kiezen
          economy = r.find_element(By.CSS_SELECTOR, "pres-avail-class-info.cabin")
          
          #prijs
          #mogelijks werkende? testen wanneer land met niet beschikbare vlucht
          try:
            prijs = economy.find_element(By.CSS_SELECTOR, "label.cabinPrice")
            prijs2 = prijs.text.split(" ")
            prijsresult = prijs2[1] + " " + prijs2[2]
          except:
            prijsresult = -1

          #stoelen
          try:
            stoelen = economy.find_element(By.CSS_SELECTOR, "div.seats")
            stoelen2 = stoelen.text.split(" ")
            stoelenresult = stoelen2[0]
          except:
            stoelenresult = -1

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

          #Flightnummers
          Flightnummers = r.find_elements(By.CSS_SELECTOR, "div.availInfoAirlineContainer div.flightNumber")
          setNummers= set()
          for x in Flightnummers:
            setNummers.add(x.text)

          #uitvoerders vluchten
          Uitvoerders = r.find_elements(By.CSS_SELECTOR, "div.availInfoAirlineContainer div.airlineName")
          setUitvoerders= set()
          for x in Uitvoerders :
            setUitvoerders.add(x.text)

          print("\ndatum:", date.today(),  "   start:", start, "   stop:", stop, "\nVertrek uur:", startUur, "  Aankomst uur:", aankomstUur, " duur:", duur.text, "\nprijs:", prijsresult, " stoelen:", stoelenresult, "\nstops:", stopresult, " tussenstop Vliegvelden:", setStops, " FlightNummers:", setNummers, " Uitvoerders:", setUitvoerders)


          #add data to datafram
          df = pd.DataFrame({
            'datum': [date.today()],
            'start': [start],
            'stop': [stop],
            'Vertrek uur':[startUur],
            'Aankomst uur':[aankomstUur],
            'duur':[duur.text],
            'prijs':[prijsresult],
            'stoelen':[stoelenresult],
            'stops':[stopresult],
            'tussenstop Viegvelden':[setStops],
            'FlightNummers':[setNummers],
            'Uitvoerders':[setUitvoerders]
          })
          #voeg dataframes samen
          dfinal = pd.concat([dfinal,df],ignore_index = True)
          

    except:
      opnieuw = True
dfinal.to_csv('scraping/brusselsAirlines.csv', index=False)

driver.quit()