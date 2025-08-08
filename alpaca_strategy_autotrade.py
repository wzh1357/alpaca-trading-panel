# alpaca_strategy_autotrade.py
import streamlit as st
import alpaca_trade_api as tradeapi

def show_autotrade_ui(api_key, api_secret, base_url):
    st.subheader("🚀 自动挂单交易")

    if not api_key or not api_secret:
        st.warning("⚠️ 请先在左侧栏输入 API Key 并连接")
        return

    # 连接 Alpaca API
    try:
        api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
        account = api.get_account()
        st.success(f"✅ 已连接账户: {account.id}")
    except Exception as e:
        st.error(f"❌ 连接失败: {e}")
        return

    st.markdown("### 🔹 配置挂单")

    symbols = st.text_area("股票代码列表 (\u9017\u53f7\u5206\u9694)", "NVDA,AMD,DUOL").split(",")
    qty = st.number_input("购买股数", 1, 100, value=10)
    buy_price = st.number_input("限价买入价", min_value=0.0)
    tp = st.number_input("TP - 止盈价", min_value=0.0)
    sl = st.number_input("SL - 止损价", min_value=0.0)

    if st.button("📈 提交挂单"):
        if not symbols or not buy_price or not tp or not sl:
            st.error("请填写完整挂单信息")
            return

        for sym in symbols:
            sym = sym.strip().upper()
            try:
                api.submit_order(
                    symbol=sym,
                    qty=qty,
                    side="buy",
                    type="limit",
                    limit_price=buy_price,
                    time_in_force="gtc",
                    order_class="bracket",
                    take_profit={"limit_price": tp},
                    stop_loss={"stop_price": sl}
                )
                st.success(f"✅ {sym} 挂单成功")
            except Exception as e:
                st.error(f"❌ {sym} 挂单失败: {e}")
