from binance.client import Client
import time

APIKey = "nx9uH5si4TE6TnILIdyVtv21MHwndLhMVLfbGak7mWcKuQwAdbypMx12c5c8WcOx"
SecretKey = "p52KWkN89JhDKpdUIqJ4kLQtDI2bQL4yUMup0O9vK67ogySDvFZVEJVoexxasHvy"

def GetCurrentPrice(symbol):
    ticket = client.get_symbol_ticker(symbol = symbol)
    return float(ticket['price'])

def PlaceBuyOrder(symbol, quantity):
    order = client.order_market_buy(symbol = symbol, quantity = quantity)
    print(f"Buy order completed: {order}")

def PlaceSellOrder(symbol, quantity):
    order = client.order_market_sell(symbol = symbol, quantity = quantity)
    print(f'Sell order completed: {order}')

def TradingBot(inPosition):
    currentPrice = GetCurrentPrice(symbol)

    while True:
        currentPrice = GetCurrentPrice(symbol)
        print(f"Current price of {symbol}: {currentPrice}")

        if not inPosition:
            if currentPrice <= buyPriceThreshold:
                PlaceBuyOrder(symbol, tradeQuantity)
                inPosition = True
                print(f'Price dropped below {buyPriceThreshold}. Placing buy order')

        else:
            if currentPrice > sellPriceThreshold:
                PlaceSellOrder(symbol, tradeQuantity)
                inPosition = False
                print(f'Price rose above {sellPriceThreshold}. Placing sell order')

        time.sleep(3)

client = Client(APIKey, SecretKey)
client.get_account()

buyPriceThreshold = 0.259
sellPriceThreshold = 0.265
tradeQuantity = 20
symbol = 'MINAUSDT'
