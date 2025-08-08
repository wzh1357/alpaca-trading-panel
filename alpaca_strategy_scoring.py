import streamlit as st
import pandas as pd
import alpaca_trade_api as tradeapi
import os

# Alpaca API 凭证（建议部署平台用环境变量管理）
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY") or "YOUR_API_KEY"
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY") or "YOUR_SECRET_KEY"
BASE_URL = os.getenv("ALPACA_BASE_URL") or "https://paper-api.alpaca.markets"

# 初始化 API 客户端
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version='v2')

# 下单函数
def place_order(symbol, side, qty):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        st.success(f"✅ 已下单 {side.upper()}：{symbol}，数量：{qty}")
    except Exception as e:
        st.error(f"❌ 下单失败：{e}")

# UI 主函数
def show_scoring_ui():
    st.subheader("📊 策略评分系统")
    st.write("显示每只股票的综合评分、买入卖出建议")

    dummy_data = pd.DataFrame({
        "股票代码": ["NVDA", "AMD", "AAPL"],
        "EMA评分": [85, 78, 90],
        "MACD评分": [75, 60, 88],
        "布林突破": ["是", "否", "是"],
        "综合建议": ["买入", "观望", "买入"]
    })
    st.dataframe(dummy_data)

    auto_trade = st.checkbox("☑️ 启用自动交易")
    if auto_trade:
        for i, row in dummy_data.iterrows():
            if row["综合建议"] == "买入":
                place_order(row["股票代码"], "buy", 10)
            elif row["综合建议"] == "卖出":
                place_order(row["股票代码"], "sell", 10)
