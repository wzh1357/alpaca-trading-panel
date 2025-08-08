
# ✅ alpaca_backtest.py
# 回测评分策略在历史数据的表现：收益曲线、胜率、最大回撤
import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="📈 策略评分回测系统", layout="wide")
st.title("📈 策略评分回测引擎")
st.caption("回测 EMA/布林/RSI+MACD 策略组合在历史数据中的收益表现")

# ========== 输入参数 ==========
symbol = st.text_input("股票代码", "NVDA").upper()
start = st.date_input("开始时间", pd.to_datetime("2022-01-01"))
end = st.date_input("结束时间", pd.to_datetime("today"))
initial_cash = st.number_input("初始资金", 10000)

# ========== 获取数据 ==========
@st.cache_data
def load_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df.dropna(inplace=True)
    return df

df = load_data(symbol, start, end)

# ========== 打分 & 信号 ==========
df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
df["bb_high"] = ta.volatility.BollingerBands(df["Close"]).bollinger_hband()
df["rsi"] = ta.momentum.rsi(df["Close"], window=14)
df["macd"] = ta.trend.macd_diff(df["Close"])

df["Score"] = 0
df["Score"] += ((df["Close"] > df["EMA50"]) & (df["Close"] < df["EMA20"])).astype(int)
df["Score"] += (df["Close"] > df["bb_high"]).astype(int)
df["Score"] += ((df["rsi"] < 30) & (df["macd"] > 0)).astype(int)

# 生成交易信号
df["Signal"] = df["Score"].apply(lambda x: 1 if x >= 2 else 0)

# ========== 回测逻辑 ==========
position = 0
cash = initial_cash
entry_price = 0
portfolio = []

for i in range(1, len(df)):
    if position == 0 and df["Signal"].iloc[i] == 1:
        entry_price = df["Close"].iloc[i]
        position = cash / entry_price
        cash = 0
        df.loc[df.index[i], "Action"] = "Buy"
    elif position > 0 and df["Signal"].iloc[i] == 0:
        cash = position * df["Close"].iloc[i]
        position = 0
        df.loc[df.index[i], "Action"] = "Sell"
    portfolio_value = cash + (position * df["Close"].iloc[i] if position > 0 else 0)
    portfolio.append(portfolio_value)

df = df.iloc[-len(portfolio):]
df["Portfolio"] = portfolio
df["Return"] = df["Portfolio"].pct_change().fillna(0)
df["Cumulative"] = (1 + df["Return"]).cumprod() * initial_cash

# ========== 图表展示 ==========
st.line_chart(df.set_index(df.index)["Cumulative"])
st.dataframe(df[["Close", "Score", "Signal", "Action", "Portfolio"]].dropna().tail(20))

# ========== 性能指标 ==========
total_return = df["Cumulative"].iloc[-1] - initial_cash
max_drawdown = (df["Cumulative"].cummax() - df["Cumulative"]).max()
win_trades = df["Action"].value_counts().get("Sell", 0)
total_trades = df["Action"].value_counts().sum() // 2
win_rate = f"{round((win_trades / total_trades) * 100, 2)}%" if total_trades > 0 else "N/A"

st.subheader("📊 回测表现")
st.markdown(f"- 总收益：${total_return:,.2f}")
st.markdown(f"- 最大回撤：${max_drawdown:,.2f}")
st.markdown(f"- 胜率：{win_rate}")
st.markdown(f"- 交易次数：{total_trades}")
