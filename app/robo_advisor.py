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

# function for symbol inputs like this: 'ad42'
def num_there(s):
    return any(i.isdigit() for i in s)

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

# empty list for multiple stocks
stocks = []

stock_num = input("Welcome to the robo-advisor!\nHow many stocks would you like to test?")

if num_there(stock_num):

    if stock_num.isnumeric(): #still need to fix for input like ad34
        stock_num = eval(stock_num)
        for i in range(1, stock_num + 1):
            symbol = input("Please enter your desired stock symbol #" + str(i) + ":\n")
            if len(symbol) > 5 or num_there(symbol):
                print("Invalid symbol. Input will be discarded.")
            else:
                stocks.append(symbol)
        print(stocks)
    else:
        print("Invalid symbol. Restarting program...")

else:
    print("Invalid symbol. Restarting program...")

for symbol in stocks:

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

    # for comparing latest close to recent 80% of recent high
    HIGHthreshold = recent_high * (8/10)

    # for comparing low
    LOWthreshold = recent_low * 1.2

    if eval(latest_close) < HIGHthreshold and eval(latest_close) > LOWthreshold:
        recommendation = "HOLD"
        reason = "STOCK IS LESS THAN 80% OF THE RECENT HIGH AND MORE THAN 120% OF THE RECENT LOW"
    elif eval(latest_close) >= HIGHthreshold:
        recommendation = "SELL!"
        reason = "STOCK IS OVERVALUED BECAUSE IT IS GREATER THAN 80% OF THE RECENT HIGH" 
    elif eval(latest_close) <= LOWthreshold:
        recommendation = "BUY!"
        reason = "STOCK IS UNDERVALUED BECAUSE IT IS WITHIN 120% OF THE RECENT LOW"

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
    print("RECOMMENDATION: " + recommendation)
    print("RECOMMENDATION REASON: " + reason)
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    # csv stuff
    file = "prices_" + symbol + ".csv"
    filename = open(file, 'w+')

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

        








