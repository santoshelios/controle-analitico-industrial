import streamlit as st

from pages.login import show_login

from pages.dashboard import show_dashboard
from pages.parameters import show_parameters
from pages.collection_points import show_collection_points
from pages.new_collection import show_new_collection
from pages.history import show_history
from pages.audit import show_audit

from services.date_filter_service import (
    inicializar_periodo,
    render_filtro_periodo
)

from pages.manager_dashboard import (
    show_manager_dashboard
)

from pages.corporate_registry import (
    show_corporate_registry
)

from pages.user_management import (
    show_user_management
)

from pages.trend_analysis import (
    show_trend_analysis
)


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(

    page_title="Industrial Control",

    page_icon="🏭",

    layout="wide",

    initial_sidebar_state="expanded"
)

# =========================================================
# CSS GLOBAL ISA
# =========================================================

st.markdown("""

<style>

.stApp {
    background: #1E1E1E;
    color: #D9D9D9;
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
    color: #D9D9D9;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    width: 330px !important;
    background: #252526;
    border-right: 1px solid #3A3A3A;
}

[data-testid="stSidebarNav"] {
    display: none;
}

[data-testid="stSidebar"] * {
    color: #D9D9D9;
}

/* BOTÕES */

.stButton > button {

    width: 100%;
    height: 50px;

    border-radius: 10px;

    border: 1px solid #3A3A3A;

    background: #2D2D30 !important;

    color: #D9D9D9 !important;

    font-weight: 600;

    transition: all 0.2s ease;

    box-shadow: none;
}

.stButton > button:hover {

    background: #3A3A3A !important;

    border: 1px solid #5A5A5A;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {

    background: #2D2D30 !important;

    border: 1px solid #3A3A3A !important;

    border-radius: 8px !important;

    color: #D9D9D9 !important;
}

/* METRICS */

div[data-testid="metric-container"] {

    background: #252526 !important;

    border: 1px solid #3A3A3A !important;

    border-radius: 10px !important;

    padding: 20px !important;

    box-shadow: none !important;
}

/* TABELAS */

table {

    background: #252526 !important;

    color: #D9D9D9 !important;
}

/* STATUS */

.status {

    display: inline-block;

    padding: 8px 14px;

    margin-right: 10px;

    margin-bottom: 12px;

    border-radius: 8px;

    background: #2D2D30;

    border: 1px solid #3A3A3A;

    color: #BFBFBF;

    font-size: 12px;

    font-weight: 600;
}

/* TITLES */

.main-title {

    font-size: 48px;

    font-weight: 800;

    color: #F2F2F2;
}

.main-subtitle {

    font-size: 17px;

    color: #A0A0A0;
}

/* PLOTLY */

.js-plotly-plot {

    border: 1px solid #3A3A3A;

    border-radius: 12px;

    background: #252526;
}

</style>

""", unsafe_allow_html=True)

# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "current_page" not in st.session_state:

    st.session_state.current_page = "dashboard"

# =========================================================
# ENGINE TEMPORAL
# =========================================================

inicializar_periodo()

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    show_login()

# =========================================================
# SISTEMA
# =========================================================

else:

    role = st.session_state.get(
        "role",
        "operador"
    )

    with st.sidebar:

        st.markdown("""

        # 🏭 Industrial Control

        Industrial Analytics Platform

        """)

        st.divider()

        st.success(
            f"Usuário ativo: {st.session_state['user_name']}"
        )

        st.divider()

        render_filtro_periodo()

        st.divider()

        st.subheader("Navegação")

        # MASTER

        if role == "master":

            if st.button("📊 Dashboard"):
                st.session_state.current_page = "dashboard"

            if st.button("📈 Dashboard Gerencial"):
                st.session_state.current_page = "manager_dashboard"

            if st.button("🧪 Parâmetros"):
                st.session_state.current_page = "parameters"

            if st.button("📍 Pontos de Coleta"):
                st.session_state.current_page = "collection_points"

            if st.button("🧫 Nova Coleta"):
                st.session_state.current_page = "new_collection"

            if st.button("📚 Histórico"):
                st.session_state.current_page = "history"

            if st.button("📈 Trend Analysis"):
                st.session_state.current_page = "trend_analysis"

            if st.button("📜 Auditoria"):
                st.session_state.current_page = "audit"

            if st.button("⚙️ Cadastros Corporativos"):
                st.session_state.current_page = "corporate_registry"

            if st.button("👥 Gestão de Usuários"):
                st.session_state.current_page = "user_management"

        else:

            if st.button("📊 Dashboard"):
                st.session_state.current_page = "dashboard"

            if st.button("📈 Dashboard Gerencial"):
                st.session_state.current_page = "manager_dashboard"

            if st.button("🧫 Nova Coleta"):
                st.session_state.current_page = "new_collection"

            if st.button("📚 Histórico"):
                st.session_state.current_page = "history"

            if st.button("📈 Trend Analysis"):
                st.session_state.current_page = "trend_analysis"

        st.divider()

        if st.button("🚪 SAIR DO SISTEMA"):

            st.session_state.clear()

            st.rerun()

    # HEADER

    st.markdown("""

    <div class="status">
    🟢 Sistema Operacional
    </div>

    <div class="status">
    ⚠ Monitoramento Ativo
    </div>

    <div class="status">
    🔒 Segurança Industrial
    </div>

    <div class="status">
    📊 Analytics Online
    </div>

    """, unsafe_allow_html=True)

    st.markdown("""

    <div class="main-title">
    Controle Analítico Industrial
    </div>

    """, unsafe_allow_html=True)

    st.markdown("""

    <div class="main-subtitle">
    Plataforma corporativa para monitoramento,
    rastreabilidade e inteligência operacional.
    </div>

    """, unsafe_allow_html=True)

    # PÁGINAS

    if st.session_state.current_page == "dashboard":

        show_dashboard()

    elif st.session_state.current_page == "parameters":

        show_parameters()

    elif st.session_state.current_page == "collection_points":

        show_collection_points()

    elif st.session_state.current_page == "new_collection":

        show_new_collection()

    elif st.session_state.current_page == "history":

        show_history()

    elif st.session_state.current_page == "audit":

        show_audit()

    elif st.session_state.current_page == "manager_dashboard":

        show_manager_dashboard()

    elif st.session_state.current_page == "corporate_registry":

        show_corporate_registry()

    elif st.session_state.current_page == "user_management":

        show_user_management()

    elif st.session_state.current_page == "trend_analysis":

        show_trend_analysis()