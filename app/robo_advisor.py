# app/robo_advisor.py
import requests
import json
import os
import csv # for prices.csv
import datetime # for date and time 
from dotenv import load_dotenv

# date and time calculations
now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")

load_dotenv() # load env

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

symbol = input("Welcome to the robo-advisor\nPlease enter your desired stock symbol: \n")

symbol = symbol.upper()

if len(symbol) != 4 or symbol.isnumeric():
    print("THIS IS WRONG")

else:

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"

    response = requests.get(request_url)

    parsed_response = json.loads(response.text)

    last_refresed = parsed_response["Meta Data"]["3. Last Refreshed"]

    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys())

    latest_day = dates[0]

    latest_close = tsd[latest_day]["4. close"]

    high_prices = []
    low_prices = [] 

    for date in dates:
        high_price = tsd[date]["2. high"]
        low_price = tsd[date]["3. low"]
        high_prices.append(float(high_price))
        low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)

    print("-------------------------")
    print("SELECTED SYMBOL:",symbol)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT:", now)
    print("-------------------------")
    print(f"LATEST DAY: {last_refresed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: TODO")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    # csv stuff
    filename = open("prices.csv", 'w+')

    filename.write('timestamp, open, high, low, close, volume\n')

    for date in dates:
        filename.write(date)
        filename.write(", ")
        filename.write(tsd[date]["1. open"])
        filename.write(", ")
        filename.write(tsd[date]["2. high"])
        filename.write(", ")
        filename.write(tsd[date]["3. low"])
        filename.write(", ")
        filename.write(tsd[date]["4. close"])
        filename.write(", ")
        filename.write(tsd[date]["5. volume"])
        filename.write("\n")

    #filename.write(parsed_response["Meta Data"]["Time Series (Daily)"])

    #filename.write(parsed_response["Meta Data"]["3. Last Refreshed"])

    








