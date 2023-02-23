# https://www.ryanair.com/gb/en

from bs4 import BeautifulSoup
import requests
import json

def createUrl():
    baseUrl = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?"
    # Request parameters: 
    # ADT -> Adults
    adt = 1
    # CHD -> Children
    chd = 0
    # DateIn -> %Y-%m-%d
    
    # DateOut -> %Y-%m-%d
    # Destination -> Airport code
    # Disc -> Discount
    # INF -> Infants
    # Origin -> Airport code
    # TEEN -> Teenagers
    # promoCode -> Promo code
    # IncludeConnectingFlights -> True/False
    # FlexDaysBeforeOut -> 0-3
    # FlexDaysOut -> 0-3
    # FlexDaysBeforeIn -> 0-3
    # FlexDaysIn -> 0-3
    # RoundTrip -> True/False
    # ToUs -> AGREED
    return baseUrl
def getData():
    URL = createUrl()
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    result = soup.find("p").text
    json_object = json.loads(result)
    return json_object

print(getData())
