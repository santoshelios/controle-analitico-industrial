import streamlit as st
import pandas as pd


# =========================================================
# PREMIUM TABLE
# =========================================================

def render_premium_table(df):

    if df.empty:

        st.info("Nenhum dado disponível.")

        return

    st.markdown("""

    <style>

    .premium-table {

        width: 100%;
        border-collapse: collapse;

        background:
            rgba(15,23,42,0.96);

        border-radius: 18px;

        overflow: hidden;

        color: white;

        font-size: 14px;
    }

    .premium-table thead {

        background:
            linear-gradient(
                90deg,
                rgba(30,41,59,1),
                rgba(51,65,85,1)
            );
    }

    .premium-table th {

        padding: 14px;

        text-align: left;

        font-weight: 700;

        color:
            rgba(255,255,255,0.92);

        border-bottom:
            1px solid rgba(255,255,255,0.06);
    }

    .premium-table td {

        padding: 14px;

        border-bottom:
            1px solid rgba(255,255,255,0.04);

        color:
            rgba(255,255,255,0.88);
    }

    .premium-table tbody tr {

        background:
            rgba(15,23,42,0.75);

        transition:
            all 0.2s ease;
    }

    .premium-table tbody tr:nth-child(even) {

        background:
            rgba(30,41,59,0.65);
    }

    .premium-table tbody tr:hover {

        background:
            rgba(37,99,235,0.25);
    }

    </style>

    """, unsafe_allow_html=True)

    html_table = """

<table class="premium-table">

<thead>

<tr>
"""

    for coluna in df.columns:

        html_table += f"<th>{coluna}</th>"

    html_table += """

</tr>

</thead>

<tbody>
"""

    for _, row in df.iterrows():

        html_table += "<tr>"

        for valor in row:

            html_table += f"<td>{valor}</td>"

        html_table += "</tr>"

    html_table += """

</tbody>

</table>
"""

    st.markdown(

        html_table,

        unsafe_allow_html=True
    )