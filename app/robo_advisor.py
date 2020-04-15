#TODO: 52 week high and low

# app/robo_advisor.py
import requests
import json
import os
import csv # for prices.csv
import datetime # for date and time 
from twilio.rest import Client # twilio stuff
from dotenv import load_dotenv

import plotly #plotly graph
import plotly.graph_objects as go #plotly graph, ADD TO README


API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

def get_response(symbol, API_KEY):
    """Returns parsed response from requested stock symbol"""
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(parsed_response):
    """Returns TSD data of the parsed response"""
    tsd = parsed_response["Time Series (Daily)"]

    rows = []
    for date, daily_prices in tsd.items():
        row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        rows.append(row)

    return rows

def to_usd(my_price):
    """Converts number into US Dollar format"""
    return "${0:,.2f}".format(my_price)

# function for symbol inputs like this: 'ad42'
def num_there(s):
    """Returns True if there is a number in the string parameter"""
    return any(i.isdigit() for i in s)

# needed to remove from global scopep
if __name__ == "__main__":
    # date and time calculations
    now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")

    load_dotenv() # load env

    # empty list for multiple stocks
    stocks = []

    stock_num = input("\nWelcome to the robo-advisor!\n\nHow many stocks would you like to evaluate?\n\n***> Disclaimer: you may only enter 5 stocks per request <***\n\nEnter Number Here: ")



    if stock_num == '0':
        print("You must enter a number higher than 0. Please try again.")

    elif num_there(stock_num):

        if stock_num.isnumeric(): #still need to fix for input like ad34
            stock_num = eval(stock_num)
            if stock_num > 5:
                print("You must enter less than 5 stocks.")

            else:
                for i in range(1, stock_num + 1):
                    symbol = input("Please enter your desired stock symbol #" + str(i) + ":\n")
                    if len(symbol) > 5 or num_there(symbol):
                        print("Invalid symbol. Input will be discarded.")
                    else:
                        stocks.append(symbol)
        else:
            print("Invalid symbol. Restarting program...")

    else:
        print("Invalid symbol. Restarting program...")

    for symbol in stocks:

        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={API_KEY}" # change to weekly

        response = requests.get(request_url)

        parsed_response = json.loads(response.text)

        last_refresed = parsed_response["Meta Data"]["3. Last Refreshed"]

        wts = parsed_response["Weekly Time Series"]

        dates = list(wts.keys())

        latest_day = dates[0]

        latest_close = wts[latest_day]["4. close"]

        second_latest_week = dates[1]

        second_latest_close = wts[second_latest_week]["4. close"]

        high_prices = []
        low_prices = [] 
        closes = []

        for date in dates[0:52]: #0-52 for the 52 week time stamp
            high_price = wts[date]["2. high"]
            low_price = wts[date]["3. low"]
            close = wts[date]["4. close"]
            high_prices.append(float(high_price))
            low_prices.append(float(low_price))
            closes.append(close)

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
        print(f"52-WEEK HIGH: {to_usd(float(recent_high))}")
        print(f"52-WEEK LOW: {to_usd(float(recent_low))}")
        print("-------------------------")
        print("RECOMMENDATION: " + recommendation)
        print("RECOMMENDATION REASON: " + reason)
        print("-------------------------")
        print("HAPPY INVESTING!")
        print("-------------------------")

        # csv stuff
        file = "data/prices_" + symbol + ".csv"

        with open(file, 'w+') as csvfile:
            csvfile.write('timestamp, open, high, low, close, volume\n')

            for date in dates[0:52]:
                csvfile.write(date)
                csvfile.write(", ")
                csvfile.write(wts[date]["1. open"])
                csvfile.write(", ")
                csvfile.write(wts[date]["2. high"])
                csvfile.write(", ")
                csvfile.write(wts[date]["3. low"])
                csvfile.write(", ")
                csvfile.write(wts[date]["4. close"])
                csvfile.write(", ")
                csvfile.write(wts[date]["5. volume"])
                csvfile.write("\n")

        TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
        TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
        SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
        RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")



        # OUTPUT FOR USER'S SMS
        price_increase = (eval(second_latest_close) * 1.05)
        price_decrease = (eval(second_latest_close) * .95)

        # COMPILE REQUEST PARAMETERS (PREPARE THE MESSAGE)
        if eval(latest_close) >= price_increase:
            content = "Wow! The latest closing price for " + symbol.upper() + " has spiked 5% or more since the last closing week!"
        elif eval(latest_close) <= price_decrease:
            content = "Uh oh, the latest closing price for " + symbol.upper() + " has dropped 5% or more since the last closing week!"
        else:
            content = "The price for " + symbol.upper() + " has been steady since the past closing week, maintaining no more than 5% growth or decline since."

        # AUTHENTICATE
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # ISSUE REQUEST (SEND SMS)
        message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)

        # plotly stuff
        # produces different graph in different window for each ticker symbol entered
        fig = go.Figure()

        # Create and style traces
        fig.add_trace(go.Scatter(x=dates, y=closes, name=symbol, line = dict(color='firebrick', width=4, dash='dot')))
            
        # Edit the layout
        fig.update_layout(title=symbol.upper() + ' Prices Over the Past 52 Weeks', xaxis_title='Time', yaxis_title='Price')


        fig.show()





