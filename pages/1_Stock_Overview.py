import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from config.settings import get_database_url


st.set_page_config(page_title="Stock Overview", layout="wide")

st.title("Stock Overview")
st.write("科技股價格走勢與波動分析")


def sample_data():
    return pd.DataFrame({
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


@st.cache_data(ttl=3600)
def load_data():
    database_url = get_database_url()

    if not database_url:
        return sample_data(), "demo_no_url"

    try:
        engine = create_engine(database_url, pool_pre_ping=True)

        query = """
        SELECT
            date,
            ticker,
            close,
            daily_return,
            ma_7,
            ma_30,
            volatility_7,
            volume
        FROM stock_prices
        ORDER BY date ASC
        """

        df = pd.read_sql(query, engine)

        if df.empty:
            return sample_data(), "demo_empty_database"

        df["date"] = pd.to_datetime(df["date"])
        return df, "database"

    except Exception as e:
        return sample_data(), "demo_error"


df, mode = load_data()

if mode == "database":
    st.success("目前使用雲端資料庫中的真實資料。")
elif mode == "demo_no_url":
    st.warning("尚未設定 DATABASE_URL，目前使用 Demo 資料。")
elif mode == "demo_empty_database":
    st.warning("雲端資料庫已連線，但 stock_prices 資料表目前沒有資料，因此使用 Demo 資料。")
else:
    st.warning("雲端資料庫連線或查詢失敗，目前使用 Demo 資料。")

st.subheader("資料預覽")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("資料來源", "Cloud DB" if mode == "database" else "Demo")

with col2:
    st.metric("股票數量", df["ticker"].nunique())

with col3:
    st.metric("資料筆數", len(df))

tickers = sorted(df["ticker"].unique())

selected_tickers = st.multiselect(
    "選擇股票代碼",
    tickers,
    default=tickers
)

filtered_df = df[df["ticker"].isin(selected_tickers)]

st.subheader("科技股收盤價走勢")

fig = px.line(
    filtered_df,
    x="date",
    y="close",
    color="ticker",
    title="Major Technology Stock Price Trend"
)

st.plotly_chart(fig, use_container_width=True)

if mode == "database":
    st.subheader("移動平均與波動率")

    selected_single_ticker = st.selectbox(
        "選擇一檔股票查看技術指標",
        tickers
    )

    indicator_df = df[df["ticker"] == selected_single_ticker].copy()

    ma_columns = []
    if "close" in indicator_df.columns:
        ma_columns.append("close")
    if "ma_7" in indicator_df.columns:
        ma_columns.append("ma_7")
    if "ma_30" in indicator_df.columns:
        ma_columns.append("ma_30")

    if ma_columns:
        ma_df = indicator_df[["date"] + ma_columns].melt(
            id_vars="date",
            var_name="indicator",
            value_name="value"
        )

        fig_ma = px.line(
            ma_df,
            x="date",
            y="value",
            color="indicator",
            title=f"{selected_single_ticker} 收盤價與移動平均"
        )

        st.plotly_chart(fig_ma, use_container_width=True)

    if "volatility_7" in indicator_df.columns:
        fig_vol = px.line(
            indicator_df,
            x="date",
            y="volatility_7",
            title=f"{selected_single_ticker} 7 日波動率"
        )

        st.plotly_chart(fig_vol, use_container_width=True)

st.subheader("原始資料表")

st.dataframe(filtered_df, use_container_width=True)
