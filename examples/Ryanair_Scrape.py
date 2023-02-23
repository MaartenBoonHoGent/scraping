import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&promoCode=&IncludeConnectingFlights=false&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=true&ToUs=AGREED"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "lxml")
result = soup.find("p").text
print(type(result))

#convert string to  object
json_object = json.loads(result)

#check new data type
print(type(json_object))

#output
#<class 'dict'>

