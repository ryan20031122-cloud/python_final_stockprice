import os
import streamlit as st


def get_database_url():
    """
    Get DATABASE_URL from Streamlit secrets or environment variable.
    Return None if it is missing or empty.
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
