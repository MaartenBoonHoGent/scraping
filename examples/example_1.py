import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/js/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "lxml")

quotes = soup.find_all("div", class_="quote")

for q in quotes:
    quote = q.find("span", class_="text")
    print(quote.text)

