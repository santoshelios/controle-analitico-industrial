import streamlit as st
from datetime import datetime


# =========================================================
# AUDITORIA CENTRAL
# =========================================================

def registrar_auditoria(

    usuario,
    role,
    acao,
    detalhes
):

    if "audit_logs" not in st.session_state:

        st.session_state.audit_logs = []

    st.session_state.audit_logs.append({

        "timestamp": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),

        "usuario": usuario,

        "role": role,

        "acao": acao,

        "detalhes": detalhes
    })