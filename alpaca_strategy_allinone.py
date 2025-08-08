# alpaca_strategy_allinone.py
import streamlit as st
from alpaca_strategy_autotrade import show_autotrade_ui
# 可选引入其他功能模块，如回测、日志等
# from alpaca_strategy_backtest import show_backtest_ui

st.set_page_config(page_title="Alpaca 策略交易系统", layout="wide")
st.title("🧠 Alpaca 策略交易系统")

# --- API 配置 ---
st.sidebar.markdown("🔐 **API 配置**")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
account_type = st.sidebar.radio("账户模式", ["模拟账户 (Paper)", "真实账户 (Live)"])

if st.sidebar.button("🔗 连接账户"):
    if api_key and api_secret:
        st.session_state["api_key"] = api_key
        st.session_state["api_secret"] = api_secret
        st.session_state["base_url"] = (
            "https://paper-api.alpaca.markets"
            if "模拟" in account_type
            else "https://api.alpaca.markets"
        )
        st.sidebar.success("✅ API 密钥已连接")
    else:
        st.sidebar.error("❌ 请填写完整的 API Key 和 Secret")

# --- 菜单导航 ---
page = st.sidebar.radio("📋 功能菜单", ["自动挂单下单"])  # 后续可扩展更多功能页面

# --- 页面渲染 ---
if page == "自动挂单下单":
    show_autotrade_ui(
        st.session_state.get("api_key"),
        st.session_state.get("api_secret"),
        st.session_state.get("base_url"),
    )
