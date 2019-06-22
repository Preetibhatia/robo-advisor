# app/robo_advisor.py

import requests
import json 
import datetime
import csv
from dotenv import load_dotenv
import os
#import statistics
import pandas as df
load_dotenv()



API_KEY = os.environ["ALPHAVANTAGE_API_KEY"]

#using requests package to access the API
####if symbol numeric/inappropriate length prompt "Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again." 
def get_response(symbol):
    
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input_symbol}&outputsize=compact&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    if "Error Message" in parsed_response:
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

q=[]
q = df.DataFrame(tsd)
if last_close > df.q.quantile(0.9):
    print("go for it!")



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
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")