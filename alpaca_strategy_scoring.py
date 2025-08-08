
# ✅ 策略评分系统：三个策略打分 → 自动判断是否挂单
import streamlit as st
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
import ta

st.set_page_config(page_title="📊 策略评分交易系统", layout="wide")
st.title("📊 多策略评分系统")
st.caption("综合评估 EMA 回调、布林突破、RSI+MACD，自动评分决定是否挂单")

# ========== 用户设置 ==========
symbol = st.sidebar.text_input("股票代码", value="NVDA").upper()
qty = st.sidebar.number_input("买入股数", value=10, min_value=1)
start = st.sidebar.date_input("开始日期", pd.to_datetime("2024-01-01"))
end = st.sidebar.date_input("结束日期", pd.to_datetime("today"))

# ========== Alpaca 账户 ==========
st.sidebar.header("🔐 Alpaca API")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
mode = st.sidebar.selectbox("账户类型", ["模拟账户", "真实账户"])
base_url = "https://paper-api.alpaca.markets" if mode == "模拟账户" else "https://api.alpaca.markets"
api = None

if api_key and api_secret:
    try:
        api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
        st.sidebar.success("API 连接成功")
    except Exception as e:
        st.sidebar.error(f"连接失败：{e}")

# ========== 下载数据 ==========
@st.cache_data
def load_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df.dropna(inplace=True)
    return df

df = load_data(symbol, start, end)

# ========== 指标计算 ==========
score = 0
last_price = df["Close"].iloc[-1]

# EMA 回调策略打分
df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
ema_signal = (df["Close"].iloc[-1] > df["EMA50"].iloc[-1]) and (df["Close"].iloc[-1] < df["EMA20"].iloc[-1])
if ema_signal:
    score += 1

# 布林带突破策略打分
bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
bb_high = bb.bollinger_hband().iloc[-1]
bb_low = bb.bollinger_lband().iloc[-1]
bb_signal = last_price > bb_high
if bb_signal:
    score += 1

# RSI + MACD 策略打分
df["rsi"] = ta.momentum.rsi(df["Close"], window=14)
macd = ta.trend.macd_diff(df["Close"])
rsi_signal = df["rsi"].iloc[-1] < 30
macd_signal = macd.iloc[-1] > 0
rsi_macd_signal = rsi_signal and macd_signal
if rsi_macd_signal:
    score += 1

# ========== 展示评分 ==========
st.subheader(f"📊 当前评分：{score}/3")
col1, col2, col3 = st.columns(3)
col1.metric("EMA 回调", "✅" if ema_signal else "❌")
col2.metric("布林带突破", "✅" if bb_signal else "❌")
col3.metric("RSI + MACD", "✅" if rsi_macd_signal else "❌")

st.line_chart(df["Close"], use_container_width=True)

# ========== 自动挂单 ==========
if score >= 2 and api:
    st.success("🟢 策略评分通过，允许挂单")
    limit_price = st.number_input("限价买入", value=float(last_price))
    tp = st.number_input("止盈价格", value=float(limit_price * 1.1))
    sl = st.number_input("止损价格", value=float(limit_price * 0.95))

    if st.button("📤 挂单执行"):
        try:
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side="buy",
                type="limit",
                limit_price=limit_price,
                time_in_force="gtc",
                order_class="bracket",
                take_profit={"limit_price": tp},
                stop_loss={"stop_price": sl}
            )
            st.success(f"✅ {symbol} 挂单成功：{limit_price} 止盈 {tp} 止损 {sl}")
        except Exception as e:
            st.error(f"挂单失败：{e}")
else:
    st.warning("评分未通过，未触发挂单")
