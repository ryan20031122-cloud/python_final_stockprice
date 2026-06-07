import os
import streamlit as st


def get_database_url():
    """
    從 Streamlit Secrets 或環境變數讀取 DATABASE_URL。
    如果沒有設定或是空字串，就回傳 None。
    """

    try:
        url = st.secrets.get("DATABASE_URL", None)
        if url is not None:
            url = str(url).strip()
            if url != "":
                return url
    except Exception:
        pass

    url = os.getenv("DATABASE_URL", "")
    url = str(url).strip()

    if url == "":
        return None

    return url
