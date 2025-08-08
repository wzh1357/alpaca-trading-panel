import streamlit as st
import pandas as pd

def show_backtest_ui():
    st.subheader("📉 策略历史回测")
    st.write("上传历史数据文件，回测 EMA/MACD/布林策略表现")

    uploaded = st.file_uploader("上传 CSV 数据 (需包含 Date, Close)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded, parse_dates=['Date'])
        st.line_chart(df.set_index('Date')['Close'])
        st.success("✅ 已加载数据，回测模块开发中…")