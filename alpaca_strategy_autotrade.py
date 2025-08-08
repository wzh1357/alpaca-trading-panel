# alpaca_strategy_autotrade.py
import streamlit as st
import alpaca_trade_api as tradeapi
import yfinance as yf


def score_strategy(symbol):
    try:
        df = yf.download(symbol, period="30d", interval="1d")
        df.dropna(inplace=True)
        df["MA5"] = df["Close"].rolling(window=5).mean()
        df["MA10"] = df["Close"].rolling(window=10).mean()

        if df["MA5"].iloc[-1] > df["MA10"].iloc[-1]:
            return "强烈买入 ✅"
        elif df["MA5"].iloc[-1] < df["MA10"].iloc[-1]:
            return "建议观望 ⚠️"
        else:
            return "中性 - 持有 🤔"
    except Exception as e:
        return f"评分失败: {e}"


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
    filter_by_score = st.checkbox("⚙️ 只对“强烈买入”股票执行挂单")

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

                # 显示策略评分结果
                with st.expander(f"📊 策略评分 - {symbol}"):
                    score = score_strategy(symbol)
                    st.write(score)

                if filter_by_score and "强烈买入" not in score:
                    st.info(f"⏭️ {symbol} 非强烈买入，已跳过挂单")
                    continue

                # 挂单
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

                st.success(f"✅ {order['symbol']} 挂单成功")
            except Exception as e:
                st.error(f"❌ {line} 挂单失败: {e}")
