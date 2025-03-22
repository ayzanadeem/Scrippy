from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twilio.rest import Client as TwilioClient
import os

# Load API Keys from Environment Variables (GitHub Secrets)
APIKey = os.getenv("API_KEY")
SecretKey = os.getenv("API_SECRET")

# Twilio API Credentials (from GitHub Secrets)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # e.g., whatsapp:+14155238886
MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")  # Your personal WhatsApp

# Initialize Binance & Twilio Clients
client = Client(APIKey, SecretKey)
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(message):
    """Send trade notifications via WhatsApp using Twilio API."""
    try:
        twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=MY_WHATSAPP_NUMBER
        )
        print("📩 WhatsApp notification sent.")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")

def GetCurrentPrice(symbol):
    """Fetches the current price of the given symbol."""
    try:
        ticket = client.get_symbol_ticker(symbol=symbol)
        return float(ticket['price'])
    except BinanceAPIException as e:
        send_whatsapp_message(f"⚠️ Error fetching price: {e}")
        return None

def PlaceBuyOrder(symbol, quantity):
    """Places a market buy order and checks if it was successful."""
    try:
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        if order["status"] in ["FILLED", "PARTIALLY_FILLED"]:
            send_whatsapp_message(f"✅ Buy order successful: {order}")
            return True
        else:
            send_whatsapp_message(f"⚠️ Buy order status: {order['status']}")
            return False
    except BinanceAPIException as e:
        send_whatsapp_message(f"❌ Binance API error during buy: {e}")
    except BinanceOrderException as e:
        send_whatsapp_message(f"❌ Order failed: {e}")
    return False

def PlaceSellOrder(symbol, quantity):
    """Places a market sell order and checks if it was successful."""
    try:
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        if order["status"] in ["FILLED", "PARTIALLY_FILLED"]:
            send_whatsapp_message(f"✅ Sell order successful: {order}")
            return True
        else:
            send_whatsapp_message(f"⚠️ Sell order status: {order['status']}")
            return False
    except BinanceAPIException as e:
        send_whatsapp_message(f"❌ Binance API error during sell: {e}")
    except BinanceOrderException as e:
        send_whatsapp_message(f"❌ Order failed: {e}")
    return False

def TradingBot(inPosition):
    """Main trading bot logic"""
    currentPrice = GetCurrentPrice(symbol)
    if currentPrice is None:
        send_whatsapp_message("Skipping this cycle due to price fetch failure.")
        return inPosition

    send_whatsapp_message(f"📈 Current price of {symbol}: {currentPrice}")

    if not inPosition:
        if currentPrice <= buyPriceThreshold:
            send_whatsapp_message(f"🔽 Price below {buyPriceThreshold}. Attempting to buy...")
            if PlaceBuyOrder(symbol, tradeQuantity):
                inPosition = True
    else:
        if currentPrice >= sellPriceThreshold:
            send_whatsapp_message(f"🔼 Price above {sellPriceThreshold}. Attempting to sell...")
            if PlaceSellOrder(symbol, tradeQuantity):
                inPosition = False

    return inPosition

# Trading parameters
buyPriceThreshold = 0.259
sellPriceThreshold = 0.265
tradeQuantity = 20
symbol = 'MINAUSDT'

# Initial position state
inPosition = False

# Run trading logic
inPosition = TradingBot(inPosition)
