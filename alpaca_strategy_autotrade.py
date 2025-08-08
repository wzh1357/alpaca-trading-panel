# alpaca_strategy_autotrade.py
import streamlit as st
import alpaca_trade_api as tradeapi

def show_autotrade_ui(api_key, api_secret, base_url):
    st.header("📈 批量挂单设置（文本输入）")

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

    st.markdown("""
    #### 格式说明：每行输入一个订单，格式如下：
    `代码, 股数, 买入价, 止盈价, 止损价`
    例如：
    ```
    NVDA,20,860,940,810
    AMD,50,160,178,148
    TSLA,20,240,270,225
    ```
    """)

    order_text = st.text_area("输入批量挂单数据", height=300)

    if st.button("📤 提交挂单"):
        st.markdown("---")
        for line in order_text.strip().split("\n"):
            try:
                parts = [x.strip() for x in line.split(",")]
                if len(parts) != 5:
                    st.warning(f"⚠️ 格式错误，跳过：{line}")
                    continue
                symbol, qty, buy_price, tp, sl = parts
                order = {
                    "symbol": symbol,
                    "qty": int(qty),
                    "buy_price": float(buy_price),
                    "tp": float(tp),
                    "sl": float(sl)
                }
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
                st.error(f"❌ {line} 挂单失败: {e}")
