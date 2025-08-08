import streamlit as st
import pandas as pd

def show_scoring_ui():
    st.subheader("📊 策略评分系统")
    st.write("显示每只股票的综合评分、买入卖出建议")

    dummy_data = pd.DataFrame({
        "股票代码": ["NVDA", "AMD", "AAPL"],
        "EMA评分": [85, 78, 90],
        "MACD评分": [75, 60, 88],
        "布林突破": ["是", "否", "是"],
        "综合建议": ["买入", "观望", "买入"]
    })
    st.dataframe(dummy_data)