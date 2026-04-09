import requests
import time

# 🔐 Telegram Bot Details
BOT_TOKEN = "8183849738:AAFlVsYDCuSLPEheQvMdyCasOjR_4D0r_Xg"
CHAT_ID = "1495582880"

# Binance API Endpoint
BASE_URL = "https://api.binance.com/api/v3/klines"

# Coins List
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT",
    "SOLUSDT", "XRPUSDT", "ADAUSDT"
]

# Timeframes
TIMEFRAMES = ["15m", "30m", "1h"]


def send_telegram_message(message):
    url = "https://api.telegram.org/bot8183849738:AAFlVsYDCuSLPEheQvMdyCasOjR_4D0r_Xg/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)


def calculate_ema(prices, period=200):
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return ema


def check_ema_signal(symbol, interval):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 210
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if not isinstance(data, list):
            print(f"API Error: {data}")
            return

        closes = [float(candle[4]) for candle in data]
        ema200 = calculate_ema(closes, 200)

        last_close = closes[-1]
        prev_close = closes[-2]

        if prev_close < ema200 and last_close > ema200:
            message = (
                f"🚀 EMA 200 Bullish Breakout\n"
                f"Symbol: {symbol}\n"
                f"Timeframe: {interval}\n"
                f"Price: {last_close:.2f}"
            )
            send_telegram_message(message)

        elif prev_close > ema200 and last_close < ema200:
            message = (
                f"🔻 EMA 200 Bearish Breakdown\n"
                f"Symbol: {symbol}\n"
                f"Timeframe: {interval}\n"
                f"Price: {last_close:.2f}"
            )
            send_telegram_message(message)

    except Exception as e:
        print(f"Error for {symbol} ({interval}): {e}")


def run_scanner():
    while True:
        print("Scanning market...")
        for symbol in SYMBOLS:
            for timeframe in TIMEFRAMES:
                check_ema_signal(symbol, timeframe)
        time.sleep(900)  # 15 minutes delay


if __name__ == "__main__":
    run_scanner()