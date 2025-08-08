# alpaca_strategy_scoring.py
import streamlit as st
import pandas as pd
import numpy as np

def show_scoring_ui(api_key=None, api_secret=None, base_url=None):
    st.header("📊 策略评分系统")

    st.markdown("此页面用于展示各种策略评分和推荐结果。")

    # 示例策略评分数据
    data = {
        "策略名称": ["EMA回调", "布林带突破", "RSI+MACD"],
        "平均收益率": [8.5, 6.2, 7.1],
        "胜率": [0.72, 0.68, 0.75],
        "推荐等级": ["⭐⭐⭐", "⭐⭐", "⭐⭐⭐"]
    }

    df = pd.DataFrame(data)

    st.dataframe(df)

    st.markdown("---")

    # 可选：评分强度判断建议
    selected_strategy = st.selectbox("选择策略查看建议", df["策略名称"])
    if selected_strategy == "EMA回调":
        st.success("📈 当前市场趋势良好，建议适度加仓 EMA 回调策略")
    elif selected_strategy == "布林带突破":
        st.info("📉 波动性增强，布林带策略可能存在虚假突破，需注意止损设置")
    elif selected_strategy == "RSI+MACD":
        st.success("✅ 多因子信号强烈，RSI+MACD 策略适合短线交易")
