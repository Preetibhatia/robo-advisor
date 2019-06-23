# app/robo_advisor.py

import requests
import json 
import datetime
import csv
from dotenv import load_dotenv
import os
#import statistics
import pandas as pd
load_dotenv()



API_KEY = os.environ["ALPHAVANTAGE_API_KEY"]

#using requests package to access the API
####if symbol numeric/inappropriate length prompt "Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again." 
def get_response(symbol):
    
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input_symbol}&outputsize=compact&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    if input_symbol.isdigit():
        print("Oh, input symbol shouldn't be a number, enter a stock symbol like 'MSFT'. Please try again.")
        exit()
    elif "Error Message" in parsed_response:
        print("Sorry, couldn't find any trading data for that symbol")
        exit() 

    return parsed_response

#1998-12-23': {'1. open': '140.3800', '2. high': '143.8100', '3. low': '139.3800', '4. close': '143.5600', '5. volume': '8735000'}
def transform_response(parsed_response):
        x=parsed_response["Time Series (Daily)"]
        rows = []
        for date, daily_prices in x.items(): 
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

def write_to_csv(rows, csa_filepath):
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in tsd:
            writer.writerow(row)
    return True

def to_usd(my_price):
    # utility function to convert float or integer to usd-formatted string (for printing)
    return "${0:,.2f}".format(my_price) #> $12,000.71

#main program
if __name__ == "__main__":
    time_now = datetime.datetime.now() 
    input_symbol = input("Please specify stock symbol (e.g AMZN) and press enter: ")
    parsed_response = get_response(input_symbol)
    tsd = transform_response(parsed_response)

latest_day = tsd[0]['timestamp']
last_close = tsd[0]['close']
high =[]
low =[]

for p in tsd:
    high.append(p['high'])
    low.append(p['low'])
recent_high = max(high)
recent_low = min(low)

#BUY-SELL Logic
df_high = pd.DataFrame(high)
df_low = pd.DataFrame(low)
high_percentile= df_high.quantile(0.8)
low_percentile =df_low.quantile(0.9)


if (int(last_close) > int(high_percentile)) and (int(last_close)>int(low_percentile)):
    action = "SELL!!"
    reason = "Price today is higher than 80 percentile of Recent High and 90 percentile of Recent Low"
else:
    action = "BUY!!"
    reason = "Price today is lower than 80 percentile of Recent High and 90 percentile of Recent Low"




csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
write_to_csv(tsd, csv_filepath)


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
print("RECOMMENDATION: ", action)
print("RECOMMENDATION REASON: ", reason)
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")