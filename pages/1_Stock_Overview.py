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


@st.cache_data
def load_data():
    database_url = get_database_url()

    if not database_url:
        return sample_data(), "demo"

    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        query = """
        SELECT date, ticker, close
        FROM stock_prices
        ORDER BY date ASC
        """
        df = pd.read_sql(query, engine)

        if df.empty:
            return sample_data(), "demo"

        return df, "database"

    except Exception:
        return sample_data(), "demo"


df, mode = load_data()

if mode == "demo":
    st.info("目前使用 Demo 資料。若要使用真實資料，請設定 DATABASE_URL 並執行 ETL pipeline。")
else:
    st.success("目前使用資料庫中的真實資料。")

fig = px.line(
    df,
    x="date",
    y="close",
    color="ticker",
    title="Major Technology Stock Price Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df, use_container_width=True)
