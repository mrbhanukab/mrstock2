import requests
from bs4 import BeautifulSoup
import asyncio

def get_data(ticker):
    url = f"https://www.marketwatch.com/investing/stock/{ticker}?countrycode=lk"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    company_name_el = soup.select_one("h1.company__name")
    company_name = company_name_el.text.strip()

    latest_update_el = soup.select_one("span.timestamp__time")
    latest_update = latest_update_el.text.strip()

    closing_price_el = soup.select_one("h2.intraday__price span.value")
    closing_price = closing_price_el.text.strip()

    previous_close_el = soup.select_one("td.u-semi")
    previous_close = previous_close_el.text.strip()

    intraday_change_el = soup.select_one("bg-quote.intraday__change")
    if intraday_change_el is not None:
        change_percent_el = intraday_change_el.select_one("span.change--percent--q")
        change_percent = change_percent_el.text.strip()
        if "positive" in intraday_change_el["class"]:
            intradaychange = f"📈 {change_percent}"
        else:
            intradaychange = f"📉 {change_percent}"
    else:
        intradaychange = "N/A"

    print(company_name, latest_update, closing_price, previous_close, intradaychange)

get_data("BOPL.N0000")