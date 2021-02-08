import requests, json

url = "https://api.upbit.com/v1/candles/minutes/1"

querystring = {"market":"KRW-BTC","count":"1"}

response = requests.request("GET", url, params=querystring)

print(response.text)
r = response.json()
r2 = r[0]["trade_price"]
print(r2)