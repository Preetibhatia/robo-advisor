# app/robo_advisor.py

import requests
import json 





#implementing user input validation logic
check = False
while check==False:
    input_symbol = input("Enter Stock symbol, e.g. 'MSFT, AAPL, GOOG, AMZN':  ")
    if input_symbol not in ('MSFT, AAPL, GOOG, AMZN'):
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
        check = False
    else:
        check = True

#using requests package to access the API
####how to pass user input in symbol?
####if symbol not found return msg "Sorry, couldn't find any trading data for that stock symbol" and exit prog 
####how to save the key in .env
#symbol=input_symbol

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=LGHZLDVZZQO2HO56"
response = requests.get(request_url)

parsed_response = json.loads(response.text)
#print(parsed_response["Meta Data"])
#print(parsed_response["Time Series (Daily)"])
parsed_response_list= []
#1998-12-23': {'1. open': '140.3800', '2. high': '143.8100', '3. low': '139.3800', '4. close': '143.5600', '5. volume': '8735000'}



for key, value in parsed_response.items():
    temp = [key,value]
    parsed_response_list.append(temp)

print(parsed_response_list)


#breakpoint()
r=[]




for p in parsed_response_list:
    r.append(p['Time Series (Daily)'])

#Key LGHZLDVZZQO2HO56




print("-------------------------")
print("SELECTED SYMBOL: ", input_symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")