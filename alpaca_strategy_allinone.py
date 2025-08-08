# alpaca_strategy_allinone.py
import streamlit as st
from alpaca_strategy_autotrade import show_autotrade_ui
from alpaca_strategy_scoring import show_scoring_ui
from alpaca_backtest import show_backtest_ui

st.set_page_config(page_title="Alpaca 自动交易系统", layout="wide")
st.title("🦰 Alpaca 策略交易系统")

# 配置 API 信息
def api_config_section():
    st.sidebar.markdown("🔐 **API 配置**")
    api_key = st.sidebar.text_input("API Key", type="password")
    api_secret = st.sidebar.text_input("API Secret", type="password")
    account_type = st.sidebar.radio("账户模式", ["模拟账户 (Paper)", "真实账户 (Live)"])

    if st.sidebar.button("🔗 请输入 API 密钥连接账户"):
        if api_key and api_secret:
            st.session_state["api_key"] = api_key
            st.session_state["api_secret"] = api_secret
            st.session_state["base_url"] = (
                "https://paper-api.alpaca.markets" if "模拟" in account_type
                else "https://api.alpaca.markets"
            )
            st.sidebar.success("✅ API 密钥已连接")
        else:
            st.sidebar.error("❌ 请填写完整的 API Key 和 Secret")

api_config_section()

# 获取配置值
api_key = st.session_state.get("api_key", "")
api_secret = st.session_state.get("api_secret", "")
base_url = st.session_state.get("base_url", "")

page = st.sidebar.radio("📋 功能菜单", ["自动挂单下单", "策略评分系统", "历史策略回测"])

if page == "自动挂单下单":
    show_autotrade_ui(api_key, api_secret, base_url)

elif page == "策略评分系统":
    show_scoring_ui(api_key, api_secret, base_url)

elif page == "历史策略回测":
    show_backtest_ui(api_key, api_secret, base_url)
