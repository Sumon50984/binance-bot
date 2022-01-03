from binance.enums import *
from binance.client import  Client
import yaml

file = "config.yml"
with open(file) as file:
   auth = yaml.load(file, Loader=yaml.FullLoader)

client = Client(api_key=auth['binance_api'], api_secret=auth['binance_secret'])

def order(pair, amount, type):
   return client.create_order(
      symbol = pair,
      side = type,
      type = 'MARKET',
      quantity = amount
   )

def price(pair):
    pair = pair.upper()
    return client.get_ticker(symbol = pair)['lastPrice']

def main(pair, amount, type):
    pair = str(pair.upper())
    last_price = price(pair)
    convert = float(amount)/float(last_price)
    convert = int(convert)
    buy = order(pair, convert, type)


def balance(coin):
    coin = coin.upper()
    bal =  client.get_asset_balance(coin)['free']
    sym = client.get_asset_balance(coin)['asset']
    if coin != "USDT":
      usd = float(bal)*float(str(price(str(coin + "USDT"))))
      text = "You have" + " " +  str(bal) + " " + str(coin) + "\n" + str(bal) + " " + str(coin) + " " +  "=" + str(usd) + " " + "USD"
      return text
    else:
      t = "You have" + " " + str(bal) + " " + "USDT"
      return t

def m_price(pair):
    pair = pair.upper()
    data = client.get_margin_price_index(symbol=pair)['price']
    return data

def m_order():
    return client.create_margin_order(
        symbol=pair,
        side=side,
        type=limit,
        timeInForce=TIME_IN_FORCE_IOC,
        quantity=amount,
        price=price
    )
