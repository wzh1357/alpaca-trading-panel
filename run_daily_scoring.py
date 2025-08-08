
# ✅ run_daily_scoring.py
# 每日定时运行评分系统，检测符合条件的股票并挂单
import pandas as pd
import yfinance as yf
import alpaca_trade_api as tradeapi
import ta
import datetime
import time

# ===== Alpaca 配置 =====
API_KEY = "YOUR_ALPACA_API_KEY"
API_SECRET = "YOUR_ALPACA_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"  # 模拟账户，实盘改为：https://api.alpaca.markets

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# ===== 股票池设置 =====
stock_list = ["NVDA", "AMD", "MSFT", "GOOGL", "DUOL"]
start = "2024-01-01"
end = str(datetime.date.today())

# ===== 打分逻辑函数 =====
def score_and_trade(symbol):
    try:
        df = yf.download(symbol, start=start, end=end)
        df.dropna(inplace=True)
        price = df["Close"].iloc[-1]

        # 策略打分
        score = 0
        df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
        df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
        if price > df["EMA50"].iloc[-1] and price < df["EMA20"].iloc[-1]:
            score += 1

        bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
        if price > bb.bollinger_hband().iloc[-1]:
            score += 1

        df["rsi"] = ta.momentum.rsi(df["Close"], window=14)
        macd = ta.trend.macd_diff(df["Close"])
        if df["rsi"].iloc[-1] < 30 and macd.iloc[-1] > 0:
            score += 1

        if score >= 2:
            # 挂单操作
            limit_price = round(price, 2)
            tp = round(limit_price * 1.1, 2)
            sl = round(limit_price * 0.95, 2)
            print(f"{symbol} ✅ 满足打分：{score}/3，挂单中...")
            api.submit_order(
                symbol=symbol,
                qty=10,
                side="buy",
                type="limit",
                limit_price=limit_price,
                time_in_force="gtc",
                order_class="bracket",
                take_profit={"limit_price": tp},
                stop_loss={"stop_price": sl}
            )
        else:
            print(f"{symbol} ❌ 打分不足（{score}/3），不挂单")
    except Exception as e:
        print(f"{symbol} 错误：{e}")

# ===== 主执行逻辑 =====
for sym in stock_list:
    score_and_trade(sym)
    time.sleep(1)
