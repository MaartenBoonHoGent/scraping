from datetime import date
import re
import time

from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from concurrent.futures import ThreadPoolExecutor



df = pd.DataFrame ({
                  'datum_extract': [],
                  'datum_vlucht': [],
                  'start': [],
                  'stop': [],
                  'Vertrek uur':[],
                  'Aankomst uur':[],
                  'duur':[],
                  'aantalStops':[],
                  'prijs':[],
                  'stoelen':[],
                  'tussenstop Viegvelden':[],
                  'FlightNummers':[],
                  'Vliegtuigen':[] })

df.to_csv('scraping/brusselsAirlines.csv', index=False)




PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

landen = ["palermo-sicilie", "faro", "alicante", "malaga", "palma-de-mallorca", "tenerife", "Kerkyra", "brindisi", "ibiza"]
maanden = ["", "", "", "APRIL", "MEI", "JUNI", "JULI", "AUGUSTUS", "SEPTEMBER", "OKTOBER"]

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


for bestemming in landen:
  # in geval van fouten opnieuw beginnen
  opnieuw = True
  #dit is om te zeggen welke datum je moet starten om te kiezen
  if(date.today().month  < 4):
    selecteerStartDag = 29
    selecteerStartMaand = 9
  else:
    selecteerStartDag = date.today().day
    selecteerStartMaand = date.today().month - 1

 
  url = f"https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-{bestemming}"
  driver.get(url)
  while(opnieuw):
    try:
      opnieuw = False
     
      WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//*[@id='flightSearch']/div[1]/div/ul/li[1]/label")))

      #enkelle reizen aanklikken 
      label_click = driver.find_element(By.CSS_SELECTOR, "label.checkbox-like.lh.lh-checkmark-checked")
      driver.execute_script("arguments[0].click()", label_click)

      #openen van info
      openen = driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[1]/div/ul/li[1]/label")
      driver.execute_script("arguments[0].click()", openen)

      WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[3]/span[1]")))

      #datum zetten
      open_dagen = driver.find_element(By.XPATH, "//*[@id='flightsTab']/div[4]/div[1]/div[1]/label")
      driver.execute_script("arguments[0].click()", open_dagen)
      #maand selecteren
      while(driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[3]/span[1]").text != '%s 2023' % maanden[selecteerStartMaand]):
        volgende = driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[2]")
        driver.execute_script("arguments[0].click()", volgende)
      #dag selecteren
      tabel = driver.find_element(By.XPATH, "//*[@id='flightSearch']/div[5]/div[3]/div[4]/table[1]")
      dagen = tabel.find_elements(By.CSS_SELECTOR, "tr.date-row td")

      #beginnen van loop
      for d in dagen:
        if(d.text == str(selecteerStartDag)):
          selecteerStartDag += 1
        
          #dag aanklikken
          driver.execute_script("arguments[0].click()", d)
          
          #klikken voor naar juiste pagina te gaan
          r = driver.find_element(By.CSS_SELECTOR, "button#searchFlights") # Findbutton by CSS selector
          driver.execute_script("arguments[0].click()", r)
          
          # wachten tot tijd geladen is
          WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[7]/div/div/footer/div[1]/lhg-upsell-back-button/button")))
          time.sleep(2)
    
          #DATA OPHALEN
          #start & stop locatie 
          locaties = driver.find_element(By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[3]/refx-page-title-pres/div/div/refx-page-title-box-pres/h1/div[2]")
          start, stop = locaties.text.split(" naar ")

          try: #er is data
            #info per reis
            reizen = driver.find_elements(By.CSS_SELECTOR, "body app refx-app-layout div div.main-content.justify-content-center refx-upsell refx-basic-in-flow-layout div div.content-wrapper div:nth-child(3) div div div refx-upsell-premium-cont refx-upsell-premium-pres mat-accordion refx-upsell-premium-row-pres")
            for r in reizen:
                #tijden voor starten en stoppen      
                startUur = r.find_element(By.CSS_SELECTOR, "div.bound-departure-datetime").text
                aankomstUur = r.find_element(By.CSS_SELECTOR, "div.bound-arrival-datetime").text
                # gedetailleerdeknop= r.find_element(By.XPATH,"/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[5]/div[3]/div/div/div/refx-upsell-premium-cont/refx-upsell-premium-pres/mat-accordion/refx-upsell-premium-row-pres[1]/div/div/refx-flight-card-pres/refx-basic-flight-card-layout/div/div/div[1]/div/div[2]/div/refx-flight-details/div/div[2]/a")
                
                vertrekDatum = r.find_element(By.XPATH, "/html/body/app/refx-app-layout/div/div[2]/refx-upsell/refx-basic-in-flow-layout/div/div[5]/div[3]/div/div/refx-calendar-cont/refx-calendar-pres/div/div/div").text

                gedetailleerdeknop = r.find_element(By.CSS_SELECTOR,"a.itin-details-link")
                driver.execute_script("arguments[0].click()", gedetailleerdeknop)

                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.itinerary-details-departure")))

                info = driver.find_element(By.CSS_SELECTOR,"div.itinerary-details-dialog-content")
                              
                listinfo=info.text.split()
                

                filterstops= re.compile(".*\(...\)")
                stops= set(filter(filterstops.match,listinfo))
                

                filterPlanes=re.compile("A[0-9]+[A-Z]*")
                planes= set(filter(filterPlanes.match,listinfo))
                

                filterFlights=re.compile("[0-9]{4}")
                flights=set(filter(filterFlights.match,listinfo))

                exitbutton= driver.find_element(By.CSS_SELECTOR,"button.mat-focus-indicator.close-btn-bottom.mat-stroked-button.mat-button-base.ng-star-inserted")
              
                driver.execute_script("arguments[0].click()", exitbutton)

                #duur
                duur = r.find_element(By.CSS_SELECTOR, "span.duration-value").text

                #Economy Classic nemen voor prijs en stoelen
                try:
                    button = r.find_element(By.CSS_SELECTOR, "button.mat-focus-indicator.flight-card-button-desktop-view.mat-button.mat-button-base.eco.ng-star-inserted")
                    driver.execute_script("arguments[0].click()", button)
                    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, "mat-expansion-panel.mat-expansion-panel")))
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

                #stops: dit zijn niet alleen maar vliegvelden maar ook stations/ deze zien we niet in de stoppen
                try:
                  Aantalstops = r.find_element(By.CSS_SELECTOR, "div.bound-nb-stop span").text
                except:
                  Aantalstops = 0
                  # print("\ndatum:", date.today(),  "   start:", start, "   stop:", stop, "\nVertrek uur:", startUur, "  Aankomst uur:", aankomstUur, " duur:", duur.text, "\nprijs:", prijsresult, " stoelen:", stoelenresult, "\nstops:", stopresult, " tussenstop Vliegvelden:", setStops, " FlightNummers:", setNummers, " Uitvoerders:", setUitvoerders)


                print("start:", start, "   stop:", stop, " duur:", duur, " \nstartUur:", startUur, " aankomstUur:", aankomstUur, " AantalStops:", Aantalstops, "\nprijs:", prijs, " stoelen:", stoelen,"VluchtCodes:",flights,"planes:",planes,"stops:",stops)
                #We krijgen een error omdat er geen dagen meer zijn waardoor 
                #de code opnieuw begint in de volgende dag/maand

                # #add data to datafram
                df2 = pd.DataFrame ({
                  'datum_extract': [date.today()],
                  'datum_vlucht': [vertrekDatum],
                  'start': [start],
                  'stop': [stop],
                  'Vertrek uur':[startUur],
                  'Aankomst uur':[aankomstUur],
                  'duur':[duur],
                  'aantalStops':[Aantalstops],
                  'prijs':[prijs],
                  'stoelen':[stoelen],
                  'tussenstop Viegvelden':[stops],
                  'FlightNummers':[flights],
                  'Vliegtuigen':[planes] })

                df2.to_csv('scraping/brusselsAirlines.csv', index=False,mode='a',header=False)
          except:
            print("geen vluchten")
      selecteerStartMaand += 1
      selecteerStartDag = 1
      if(selecteerStartMaand == 10):
        break

    #na elke dag krijgen we een except
    #en zo resetten we
    except:
      opnieuw = True
      driver.get(url)


