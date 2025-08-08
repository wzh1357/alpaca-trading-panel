import streamlit as st
from alpaca_strategy_autotrade import show_autotrade_ui
from alpaca_strategy_scoring import show_scoring_ui
from alpaca_backtest import show_backtest_ui

st.set_page_config(page_title="Alpaca 自动交易系统", layout="wide")

st.title("🧠 Alpaca 策略交易系统")

page = st.sidebar.radio("📋 功能菜单", ["自动挂单下单", "策略评分系统", "历史策略回测"])

if page == "自动挂单下单":
    show_autotrade_ui()

elif page == "策略评分系统":
    show_scoring_ui()

elif page == "历史策略回测":
    show_backtest_ui()
