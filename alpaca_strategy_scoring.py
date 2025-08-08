# alpaca_strategy_scoring.py
import streamlit as st
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD


def show_scoring_ui(api_key, api_secret, base_url):
    st.subheader("📊 策略评分系统")

    if not api_key or not api_secret:
        st.warning("⚠️ 请先在左侧输入 API Key 并连接")
        return

    try:
        api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
        account = api.get_account()
        st.success(f"✅ 已连接账户: {account.id}")
    except Exception as e:
        st.error(f"❌ 连接失败: {e}")
        return

    tickers = st.text_input("输入股票代码 (逗号分隔)", "NVDA,AMD,TSLA")
    symbols = [s.strip().upper() for s in tickers.split(",") if s.strip()]
    start_date = st.date_input("回测开始日期", pd.to_datetime("2024-01-01"))

    if st.button("📈 开始评分"):
        for symbol in symbols:
            try:
                df = yf.download(symbol, start=start_date)
                df.dropna(inplace=True)

                df['rsi'] = RSIIndicator(df['Close']).rsi()
                macd = MACD(df['Close'])
                df['macd'] = macd.macd()
                df['macd_signal'] = macd.macd_signal()

                latest = df.iloc[-1]
                rsi_score = 1 if 40 < latest['rsi'] < 60 else 0
                macd_score = 1 if latest['macd'] > latest['macd_signal'] else 0

                total_score = rsi_score + macd_score

                st.markdown(f"**{symbol} 策略评分：{total_score}/2**")
                st.progress(total_score / 2)

            except Exception as e:
                st.error(f"❌ {symbol} 评分失败: {e}")
