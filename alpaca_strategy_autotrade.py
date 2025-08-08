
# ✅ Alpaca 策略整合挂单系统：多策略选股 + 一键下单
import streamlit as st
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
import ta

st.set_page_config(page_title="策略驱动交易面板", layout="wide")
st.title("🧠 策略驱动 Alpaca 自动交易系统")
st.caption("选策略 → 选股 → 实时信号 → 一键挂单")

# ========== Alpaca API 配置 ==========
st.sidebar.header("🔐 Alpaca API 配置")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
mode = st.sidebar.selectbox("交易模式", ["模拟账户", "真实账户"])
base_url = "https://paper-api.alpaca.markets" if mode == "模拟账户" else "https://api.alpaca.markets"
api = None

if api_key and api_secret:
    try:
        api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
        account = api.get_account()
        st.sidebar.success(f"连接成功，账户余额：${account.cash}")
    except Exception as e:
        st.sidebar.error(f"连接失败：{e}")
        api = None

# ========== 策略选择 ==========
st.sidebar.header("📊 策略选择")
strategy = st.sidebar.selectbox("选择交易策略", ["EMA 回调", "布林带突破", "RSI + MACD"])
symbol = st.sidebar.text_input("股票代码", value="NVDA").upper()
qty = st.sidebar.number_input("下单数量", min_value=1, value=10)

start = st.sidebar.date_input("回测起始", pd.to_datetime("2024-01-01"))
end = st.sidebar.date_input("回测结束", pd.to_datetime("today"))

# ========== 数据获取 ==========
@st.cache_data
def load_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df.dropna(inplace=True)
    return df

df = load_data(symbol, start, end)

# ========== 策略判断 ==========
signal = ""
df["Signal"] = ""

if strategy == "EMA 回调":
    df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
    df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
    cond = (df["Close"] > df["EMA50"]) & (df["Close"] < df["EMA20"])
    df.loc[cond, "Signal"] = "✅ BUY"
    signal = df["Signal"].iloc[-1]

elif strategy == "布林带突破":
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"] = bb.bollinger_lband()
    cond = df["Close"] > df["bb_high"]
    df.loc[cond, "Signal"] = "✅ BUY"
    cond2 = df["Close"] < df["bb_low"]
    df.loc[cond2, "Signal"] = "❌ SELL"
    signal = df["Signal"].iloc[-1]

elif strategy == "RSI + MACD":
    df["rsi"] = ta.momentum.rsi(df["Close"], window=14)
    df["macd"] = ta.trend.macd_diff(df["Close"])
    cond = (df["rsi"] < 30) & (df["macd"] > 0)
    df.loc[cond, "Signal"] = "✅ BUY"
    cond2 = (df["rsi"] > 70) & (df["macd"] < 0)
    df.loc[cond2, "Signal"] = "❌ SELL"
    signal = df["Signal"].iloc[-1]

# ========== 展示图表 ==========
st.subheader(f"📈 {symbol} 策略信号：{signal if signal else '暂无信号'}")
st.dataframe(df[["Close", "Signal"]].tail(20), use_container_width=True)
st.line_chart(df["Close"], use_container_width=True)

# ========== 一键下单 ==========
if signal.startswith("✅") and api:
    price = df["Close"].iloc[-1]
    st.success(f"检测到买入信号，当前价格：${price:.2f}")
    limit_price = st.number_input("限价买入价", value=float(price))
    tp = st.number_input("止盈价", value=float(price * 1.1))
    sl = st.number_input("止损价", value=float(price * 0.95))

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
            st.success(f"{symbol} ✅ 挂单成功：限价 {limit_price}，止盈 {tp}，止损 {sl}")
        except Exception as e:
            st.error(f"挂单失败：{e}")
else:
    st.warning("暂无可执行的买入信号或未连接 API")
