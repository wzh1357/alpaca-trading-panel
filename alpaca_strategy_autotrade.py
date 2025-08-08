# alpaca_strategy_autotrade.py
import streamlit as st
import alpaca_trade_api as tradeapi


def show_autotrade_ui(api_key, api_secret, base_url):
    st.header("📈 批量挂单设置（每只股票独立配置）")

    if not api_key or not api_secret:
        st.warning("请先在左侧输入 API 密钥并连接账户")
        return

    try:
        api = tradeapi.REST(api_key, api_secret, base_url)
        account = api.get_account()
        st.success(f"✅ 已连接账户: {account.id}")
    except Exception as e:
        st.error(f"❌ API 连接失败: {e}")
        return

    with st.form("挂单配置表单"):
        stock_count = st.number_input("要挂单的股票数量", min_value=1, max_value=20, value=3)
        orders = []

        for i in range(stock_count):
            st.markdown(f"#### 🧾 股票 {i+1}")
            symbol = st.text_input(f"股票代码 {i+1}", key=f"symbol_{i}")
            qty = st.number_input(f"买入股数 {i+1}", min_value=1, value=10, key=f"qty_{i}")
            buy_price = st.number_input(f"限价买入价 {i+1}", min_value=0.0, value=0.0, key=f"buy_{i}")
            tp = st.number_input(f"TP - 止盈价 {i+1}", min_value=0.0, value=0.0, key=f"tp_{i}")
            sl = st.number_input(f"SL - 止损价 {i+1}", min_value=0.0, value=0.0, key=f"sl_{i}")
            orders.append({"symbol": symbol, "qty": qty, "buy_price": buy_price, "tp": tp, "sl": sl})

        submitted = st.form_submit_button("📤 提交挂单")

        if submitted:
            st.markdown("---")
            for order in orders:
                if not order["symbol"] or order["buy_price"] == 0:
                    st.warning(f"⚠️ 股票 {order['symbol']} 信息不完整，跳过")
                    continue
                try:
                    api.submit_order(
                        symbol=order["symbol"],
                        qty=order["qty"],
                        side="buy",
                        type="limit",
                        limit_price=order["buy_price"],
                        time_in_force="gtc",
                        order_class="bracket",
                        take_profit={"limit_price": order["tp"]},
                        stop_loss={"stop_price": order["sl"]}
                    )
                    st.success(f"✅ {order['symbol']} 挂单成功")
                except Exception as e:
                    st.error(f"❌ {order['symbol']} 挂单失败: {e}")
