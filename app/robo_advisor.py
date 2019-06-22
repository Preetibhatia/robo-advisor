# app/robo_advisor.py

import requests
import json 
import datetime
import csv
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.environ["ALPHAVANTAGE_API_KEY"]

#implementing user input validation logic
check = False
while check==False:
    input_symbol = input("Enter Stock symbol, e.g. 'MSFT, AAPL, GOOG, AMZN':  ")
    if input_symbol not in ('MSFT, AAPL, GOOG, AMZN, AXP'):
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
        check = False
    else:
        check = True

#using requests package to access the API
####if symbol not found return msg "Sorry, couldn't find any trading data for that stock symbol" and exit prog 
def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input_symbol}&outputsize=full&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

#1998-12-23': {'1. open': '140.3800', '2. high': '143.8100', '3. low': '139.3800', '4. close': '143.5600', '5. volume': '8735000'}
def transform_response(parsed_response):
        tsd=parsed_response["Time Series (Daily)"]
        
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

#main program
if __name__ == "__main__":
time_now = datetime.datetime.now() 
input_symbol = input("Please specify stock symbol (e.g AMZN) and press enter: ")
parsed_response = get_response(input_symbol)
tsd = transform_response(parsed_response)

#{'timestamp': '2019-06-19', 'open': 1105.6, 'high': 1107.0, 'low': 1093.48, 'close': 1102.33, 'volume': 1338575}

def to_usd(my_price):
    # utility function to convert float or integer to usd-formatted string (for printing)
    return "${0:,.2f}".format(my_price) #> $12,000.71

latest_day = rows[0]['timestamp']
last_close = rows[0]['close']
high =[]
low =[]
for p in rows:
    high.append(p['high'])
    low.append(p['low'])
recent_high = max(high)
recent_low = min(low)


print("-------------------------")
print("SELECTED SYMBOL: ", input_symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", time_now)
print("-------------------------")
print("LATEST DAY: ", latest_day)
print("LATEST CLOSE: ", to_usd(last_close))
print("RECENT HIGH: ", to_usd(recent_high))
print("RECENT LOW: ", to_usd(recent_low))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")