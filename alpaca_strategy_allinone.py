
# 🧠 批量评分 + 胜率回测 + 自动挂单系统入口
import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="🧠 多股策略评分系统", layout="wide")
st.title("🧠 多股批量评分 + 回测系统")
st.caption("支持股票池打分筛选、历史回测、挂单提示、自动策略执行")

# ========== 设置区域 ==========
symbols = st.text_area("📋 输入股票池（每行一个）", "NVDA\nAMD\nGOOGL\nMSFT\nDUOL").splitlines()
start = st.date_input("历史起始时间", pd.to_datetime("2024-01-01"))
end = st.date_input("历史结束时间", pd.to_datetime("today"))

# ========== 下载并评分 ==========
def score_stock(symbol, start, end):
    try:
        df = yf.download(symbol, start=start, end=end)
        df.dropna(inplace=True)

        # 评分初始化
        score = 0
        latest = df["Close"].iloc[-1]

        # EMA
        df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
        df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
        ema_signal = (latest > df["EMA50"].iloc[-1]) and (latest < df["EMA20"].iloc[-1])
        score += int(ema_signal)

        # Bollinger
        bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
        bb_high = bb.bollinger_hband().iloc[-1]
        bb_signal = latest > bb_high
        score += int(bb_signal)

        # RSI + MACD
        df["rsi"] = ta.momentum.rsi(df["Close"], window=14)
        macd = ta.trend.macd_diff(df["Close"])
        rsi_signal = df["rsi"].iloc[-1] < 30
        macd_signal = macd.iloc[-1] > 0
        score += int(rsi_signal and macd_signal)

        return {
            "代码": symbol,
            "价格": latest,
            "得分": score,
            "EMA": "✅" if ema_signal else "❌",
            "布林": "✅" if bb_signal else "❌",
            "RSI+MACD": "✅" if rsi_signal and macd_signal else "❌"
        }
    except Exception as e:
        return {
            "代码": symbol,
            "价格": None,
            "得分": 0,
            "EMA": "❌",
            "布林": "❌",
            "RSI+MACD": "❌"
        }

# ========== 批量运行 ==========
if st.button("🚀 批量评分"):
    with st.spinner("正在评分分析..."):
        results = [score_stock(sym.strip().upper(), start, end) for sym in symbols if sym.strip()]
        df_result = pd.DataFrame(results).sort_values("得分", ascending=False)
        st.dataframe(df_result, use_container_width=True)
        st.bar_chart(df_result.set_index("代码")["得分"])

        top = df_result[df_result["得分"] >= 2]
        if not top.empty:
            st.success("✅ 推荐挂单候选：")
            st.dataframe(top[["代码", "价格", "得分"]])
        else:
            st.warning("暂无合适挂单标的")

# ========== 胜率回测占位 ==========
st.markdown("---")
st.subheader("📈 胜率回测结果（示意）")
st.info("后续将接入交易回测引擎，统计得分策略历史收益、胜率、最大回撤")

# ========== 定时执行脚本（部署用） ==========
st.markdown("---")
st.subheader("⏱ 定时运行脚本部署建议")
st.code("""
# 可部署在 VPS / GitHub Actions：
python run_daily_scoring.py
# 每日开盘前执行打分 → 自动提交 Alpaca 挂单
""", language="bash")
