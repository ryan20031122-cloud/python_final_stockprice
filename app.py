import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="科技股與新聞情緒分析 Dashboard",
    layout="wide"
)

st.title("科技股與新聞情緒分析 Dashboard")
st.write("A cloud-hosted dashboard integrating stock prices, volatility indicators, and news sentiment.")

# Sample stock data for demo
stock_data = pd.DataFrame({
    "date": pd.date_range(start="2024-01-01", periods=10, freq="D").tolist() * 5,
    "ticker": ["AAPL"] * 10 + ["MSFT"] * 10 + ["NVDA"] * 10 + ["GOOGL"] * 10 + ["TSLA"] * 10,
    "close": [
        185, 187, 186, 190, 193, 195, 194, 198, 200, 202,
        370, 372, 375, 374, 380, 383, 386, 390, 392, 395,
        480, 490, 505, 520, 540, 560, 590, 610, 630, 650,
        140, 142, 141, 145, 147, 150, 149, 152, 154, 156,
        250, 245, 248, 252, 249, 255, 260, 258, 262, 265
    ]
})

sentiment_data = pd.DataFrame({
    "sentiment": ["Positive", "Neutral", "Negative"],
    "count": [18, 10, 7]
})

event_data = pd.DataFrame({
    "date": ["2024-01-03", "2024-01-05", "2024-01-08"],
    "event": [
        "AI chip demand increased",
        "Federal Reserve rate discussion",
        "Major technology earnings report"
    ],
    "related_stock": ["NVDA", "AAPL / MSFT", "TSLA"]
})

st.subheader("市場總覽")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("追蹤股票數量", "5")

with col2:
    st.metric("新聞情緒", "Positive")

with col3:
    st.metric("資料狀態", "Demo data")

st.subheader("科技股價格走勢")

fig = px.line(
    stock_data,
    x="date",
    y="close",
    color="ticker",
    title="Major Technology Stock Price Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("新聞情緒分布")

fig2 = px.pie(
    sentiment_data,
    names="sentiment",
    values="count",
    title="News Sentiment Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("股價變化與新聞 / 國際事件對照")

st.dataframe(event_data, use_container_width=True)

st.info(
    "此 Dashboard 示範如何將科技股股價、波動情形與新聞事件進行對照。"
    "未來可透過 ETL pipeline 自動抓取 Yahoo Finance 股價與新聞資料，"
    "並寫入 PostgreSQL 資料庫。"
)
