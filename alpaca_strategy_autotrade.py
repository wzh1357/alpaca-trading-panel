import streamlit as st
import pandas as pd

def show_autotrade_ui():
    st.subheader("📈 批量挂单设置")
    st.markdown("可输入多只股票，每行格式：**代码, 股数, 买入价, 止盈价, 止损价**")

    example = """
    NVDA,10,180,200,170
    AMD,5,165,185,155
    """
    st.code(example, language="text")

    order_input = st.text_area("输入挂单列表", height=200)
    if st.button("📤 提交挂单"):
        st.success("已接收挂单，准备提交")
        st.write(order_input)