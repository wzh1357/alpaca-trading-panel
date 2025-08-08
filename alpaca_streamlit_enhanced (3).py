
# ✅ Alpaca 自动挂单可视化面板（增强版）
import streamlit as st
import alpaca_trade_api as tradeapi
import pandas as pd

st.set_page_config(page_title="Alpaca 自动交易面板", layout="wide")

st.title("📈 Alpaca 自动交易挂单系统")
st.caption("支持批量挂单、多股票输入、止盈止损、订单状态查看")

# API 输入区
st.sidebar.header("🔐 API 配置")
API_KEY = st.sidebar.text_input("API Key", type="password")
API_SECRET = st.sidebar.text_input("API Secret", type="password")
mode = st.sidebar.radio("账户模式", ["模拟账户 (Paper)", "真实账户 (Live)"])

BASE_URL = "https://paper-api.alpaca.markets" if mode == "模拟账户 (Paper)" else "https://api.alpaca.markets"

# 初始化 API 客户端
if API_KEY and API_SECRET:
    try:
        api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")
        account = api.get_account()
        st.sidebar.success(f"连接成功：账户余额 ${account.cash}")
    except Exception as e:
        st.sidebar.error(f"API 连接失败：{e}")
        api = None
else:
    st.sidebar.warning("请输入 API 密钥连接账户")
    api = None

# 分栏区域
tab1, tab2 = st.tabs(["📤 下单挂单", "📋 查看订单"])

with tab1:
    st.subheader("📝 批量挂单设置")
    st.markdown("可输入多只股票，每行格式：`代码, 股数, 买入价, 止盈价, 止损价`，例如：")
    st.code("NVDA,10,180,200,170\nAMD,5,165,185,155", language="text")

    input_text = st.text_area("输入挂单列表", height=200)

    if st.button("📤 提交挂单") and api:
        lines = input_text.strip().split("\n")
        success = 0
        for line in lines:
            try:
                symbol, qty, buy, tp, sl = [x.strip().upper() for x in line.split(",")]
                api.submit_order(
                    symbol=symbol,
                    qty=int(qty),
                    side="buy",
                    type="limit",
                    limit_price=float(buy),
                    time_in_force="gtc",
                    order_class="bracket",
                    take_profit={"limit_price": float(tp)},
                    stop_loss={"stop_price": float(sl)}
                )
                st.success(f"✅ {symbol} 挂单成功")
                success += 1
            except Exception as e:
                st.error(f"❌ {line} 挂单失败: {e}")
        if success:
            st.balloons()

with tab2:
    st.subheader("📋 当前订单状态")
    if api:
        try:
            orders = api.list_orders(status="all", limit=50)
            rows = []
            for o in orders:
                rows.append({
                    "时间": o.submitted_at.strftime("%Y-%m-%d %H:%M"),
                    "代码": o.symbol,
                    "类型": o.side,
                    "数量": o.qty,
                    "状态": o.status,
                    "限价": o.limit_price,
                    "止损": getattr(o, "stop_price", None),
                    "止盈": getattr(o, "take_profit", None),
                    "成交均价": o.filled_avg_price,
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"无法获取订单信息：{e}")
    else:
        st.info("请先连接 API 查看订单")
