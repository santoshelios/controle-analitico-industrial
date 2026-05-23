import psycopg2
import streamlit as st

# =====================================================
# POSTGRESQL CONNECTION
# =====================================================

@st.cache_resource
def get_connection():

    return psycopg2.connect(

        host=st.secrets["postgres"]["host"],

        database=st.secrets["postgres"]["database"],

        user=st.secrets["postgres"]["user"],

        password=st.secrets["postgres"]["password"],

        port=st.secrets["postgres"]["port"],

        sslmode="require"
    )

# =====================================================
# SAFE CONNECTION
# =====================================================

def get_safe_connection():

    conn = get_connection()

    try:

        conn.cursor().execute(
            "SELECT 1"
        )

    except:

        get_connection.clear()

        conn = get_connection()

    return conn