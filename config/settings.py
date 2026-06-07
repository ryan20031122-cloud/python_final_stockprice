import os
import streamlit as st


def get_database_url():
    try:
        if "DATABASE_URL" in st.secrets:
            url = st.secrets["DATABASE_URL"]
            if url:
                return str(url).strip()
    except Exception:
        pass

    url = os.getenv("DATABASE_URL")
    if url:
        return url.strip()

    return None
