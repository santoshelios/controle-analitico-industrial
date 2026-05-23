import streamlit as st

from pages.login import show_login

from pages.dashboard import show_dashboard
from pages.parameters import show_parameters
from pages.collection_points import show_collection_points
from pages.new_collection import show_new_collection
from pages.history import show_history
from pages.audit import show_audit
from services.date_filter_service import(
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
# CSS GLOBAL
# =========================================================

st.markdown("""
<style>

/* =========================================================
APP
========================================================= */

.stApp {

    background:
        radial-gradient(circle at top left,
        #132238 0%,
        #020617 60%);

    color: white;
}

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {

    font-family: "Inter", sans-serif;
}

/* =========================================================
SIDEBAR
========================================================= */

[data-testid="stSidebar"] {

    width: 340px !important;

    background:
        linear-gradient(
            180deg,
            #020617 0%,
            #0F172A 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.06);

    box-shadow:
        8px 0 30px rgba(0,0,0,0.35);
}

/* TEXT */

[data-testid="stSidebar"] * {

    color: white;
}

/* REMOVE STREAMLIT NAV */

[data-testid="stSidebarNav"] {

    display: none;
}

/* SIDEBAR BUTTONS */

[data-testid="stSidebar"] .stButton {

    display: flex;

    justify-content: center;
}

[data-testid="stSidebar"] .stButton > button {

    width: 260px !important;

    min-width: 260px !important;

    max-width: 260px !important;

    height: 58px;

    min-height: 58px;

    margin-bottom: 14px;

    border-radius: 18px;

    border:
        1px solid rgba(59,130,246,0.30);

    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.95),
            rgba(29,78,216,0.92)
        ) !important;

    color:
        white !important;

    font-weight: 700;

    font-size: 15px;

    letter-spacing: 0.2px;

    text-align: left;

    padding-left: 20px;

    display: flex;

    align-items: center;

    justify-content: flex-start;

    transition:
        all 0.25s ease;

    box-shadow:
        0 12px 34px rgba(37,99,235,0.32);
}

/* FORCE BUTTON CONTENT */

[data-testid="stSidebar"] .stButton > button p {

    width: 100% !important;

    text-align: left !important;

    margin: 0 !important;
}

/* HOVER */

[data-testid="stSidebar"] .stButton > button:hover {

    transform:
        translateX(6px);

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,1),
            rgba(37,99,235,0.95)
        ) !important;

    border:
        1px solid rgba(96,165,250,0.50);

    color:
        white !important;

    box-shadow:
        0 14px 40px rgba(59,130,246,0.45);
}

/* USER BLOCK */

[data-testid="stSidebar"] .stAlert {

    background:
        rgba(37,99,235,0.10) !important;

    border:
        1px solid rgba(59,130,246,0.20) !important;

    border-radius:
        14px !important;
}
            



/* =========================================================
LABELS
========================================================= */
/* =========================================================
INPUTS
========================================================= */

/* LABELS */

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stCheckbox label,
.stTextArea label {

    color: white !important;

    font-weight: 600 !important;

    font-size: 14px !important;
}

/* TEXT INPUT */

.stTextInput input {

    background:
        rgba(15,23,42,0.95) !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;

    border-radius: 12px !important;

    color: white !important;

    height: 52px !important;
}

/* NUMBER INPUT */

.stNumberInput input {

    background:
        rgba(15,23,42,0.95) !important;

    color: white !important;

    border-radius: 12px !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;
}

/* SELECTBOX */

.stSelectbox div[data-baseweb="select"] > div {

    background:
        rgba(15,23,42,0.95) !important;

    color: white !important;

    border-radius: 12px !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;
}

/* TEXT AREA */

.stTextArea textarea {

    background:
        rgba(15,23,42,0.95) !important;

    color: white !important;

    border-radius: 12px !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;
}

/* CHECKBOX */

.stCheckbox {

    color: white !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {

    width: 100%;

    height: 52px;

    border-radius: 14px;

    border: 1px solid rgba(59,130,246,0.35);

    background:
        linear-gradient(
            135deg,
            #2563EB 0%,
            #1D4ED8 100%
        ) !important;

    color: white !important;

    font-weight: 700;

    font-size: 14px;

    cursor: pointer;

    transition: all 0.3s ease;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.35);
}

.stButton > button:hover {

    transform: translateY(-2px);

    background:
        linear-gradient(
            135deg,
            #3B82F6 0%,
            #2563EB 100%
        ) !important;

    border:
        1px solid rgba(96,165,250,0.6);

    box-shadow:
        0 14px 40px rgba(59,130,246,0.45);
}

/* =========================================================
FORM BUTTONS
========================================================= */

.stForm button {

    width: 100% !important;

    height: 52px !important;

    border-radius: 14px !important;

    border:
        1px solid rgba(59,130,246,0.35) !important;

    background:
        linear-gradient(
            135deg,
            #2563EB 0%,
            #1D4ED8 100%
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    font-size: 14px !important;

    cursor: pointer !important;

    transition: all 0.3s ease !important;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.35) !important;
}

.stForm button:hover {

    transform: translateY(-2px);

    background:
        linear-gradient(
            135deg,
            #3B82F6 0%,
            #2563EB 100%
        ) !important;

    border:
        1px solid rgba(96,165,250,0.6) !important;

    box-shadow:
        0 14px 40px rgba(59,130,246,0.45) !important;
}         


            
/* =========================================================
METRICS / KPI
========================================================= */

div[data-testid="metric-container"] {

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,0.62),
            rgba(30,41,59,0.88)
        ) !important;

    border:
        1px solid rgba(96,165,250,0.35);

    padding: 28px;

    border-radius: 22px;

    backdrop-filter: blur(12px);

    box-shadow:
        0 18px 45px rgba(37,99,235,0.28);

    transition:
        all 0.30s ease;
}

/* TOP LIGHT */

div[data-testid="metric-container"]::before {

    content: "";

    position: absolute;

    top: 0;
    left: 0;

    width: 100%;
    height: 5px;

    background:
        linear-gradient(
            90deg,
            rgba(59,130,246,0),
            rgba(96,165,250,1),
            rgba(59,130,246,0)
        );
}

/* INNER GLOW */

div[data-testid="metric-container"]::after {

    content: "";

    position: absolute;

    inset: 0;

    background:
        radial-gradient(
            circle at top left,
            rgba(96,165,250,0.14),
            transparent 60%
        );

    pointer-events: none;
}

/* HOVER */

div[data-testid="metric-container"]:hover {

    transform:
        translateY(-8px);

    border:
        1px solid rgba(96,165,250,0.50);

    box-shadow:
        0 24px 60px rgba(59,130,246,0.40);
}

/* LABEL */

div[data-testid="metric-container"] label {

    color:
        rgba(255,255,255,0.98) !important;

    font-size:
        14px !important;

    font-weight:
        800 !important;

    letter-spacing:
        0.4px;
}

/* VALUE */

div[data-testid="stMetricValue"] {

    color:
        white !important;

    font-size:
        44px !important;

    font-weight:
        900 !important;

    line-height:
        1.1;

    text-shadow:
        0 0 20px rgba(96,165,250,0.50);
}

/* DELTA */

div[data-testid="stMetricDelta"] {

    font-size:
        13px !important;

    font-weight:
        700 !important;
}

/* =========================================================
STATUS
========================================================= */

.status {

    display: inline-block;

    padding: 10px 16px;

    margin-right: 10px;

    margin-bottom: 14px;

    border-radius: 12px;

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    color: #CBD5E1;

    font-size: 13px;

    font-weight: 500;
}

/* =========================================================
TABLES
========================================================= */

/* TABLE CONTAINER */

table {

    width: 100% !important;

    border-collapse: collapse !important;

    background:
        rgba(15,23,42,0.92) !important;

    border-radius: 14px !important;

    overflow: hidden !important;

    color: white !important;

    border:
        1px solid rgba(59,130,246,0.12) !important;
}

/* HEADER */

table thead tr th {

    background:
        rgba(30,41,59,0.95) !important;

    color:
        white !important;

    font-weight:
        700 !important;

    padding:
        14px !important;

    border:
        none !important;

    text-align:
        left !important;
}

/* ROWS */

table tbody tr {

    background:
        rgba(15,23,42,0.78) !important;

    color:
        rgba(255,255,255,0.92) !important;

    transition:
        all 0.2s ease;
}

/* ZEBRA */

table tbody tr:nth-child(even) {

    background:
        rgba(30,41,59,0.42) !important;
}

/* HOVER */

table tbody tr:hover {

    background:
        rgba(59,130,246,0.18) !important;
}

/* CELLS */

table td {

    padding:
        12px !important;

    border:
        none !important;

    color:
        white !important;

    font-size:
        14px !important;
}

/* HEADER */

div[data-testid="stDataFrame"] thead tr th {

    background:
        rgba(30,41,59,0.95) !important;

    color:
        white !important;

    font-weight:
        700 !important;

    border:
        none !important;

    font-size:
        14px !important;

    padding:
        14px !important;
}

/* ROWS */

div[data-testid="stDataFrame"] tbody tr {

    background:
        rgba(15,23,42,0.78) !important;

    color:
        rgba(255,255,255,0.92) !important;

    transition:
        all 0.2s ease;
}

/* ZEBRA */

div[data-testid="stDataFrame"] tbody tr:nth-child(even) {

    background:
        rgba(30,41,59,0.45) !important;
}

/* HOVER */

div[data-testid="stDataFrame"] tbody tr:hover {

    background:
        rgba(59,130,246,0.18) !important;
}

/* CELLS */

div[data-testid="stDataFrame"] td {

    border:
        none !important;

    padding:
        12px !important;

    font-size:
        14px !important;
}            




/* =========================================================
TÍTULOS
========================================================= */

.main-title {

    font-size: 54px;

    font-weight: 800;

    line-height: 1.1;

    color: white;

    margin-top: 10px;

    margin-bottom: 12px;
}

.main-subtitle {

    font-size: 18px;

    color: #94A3B8;

    line-height: 1.8;

    max-width: 900px;

    margin-bottom: 40px;
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
# COLETAS MOCK OPERACIONAIS
# =========================================================

if "coletas" not in st.session_state:

    st.session_state.coletas = []


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

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown("""
        # 🏭 Industrial Control

        Secure Enterprise Platform
        """)

        st.divider()

        st.success(
            f"Usuário ativo: {st.session_state['user_name']}"
        )

        st.divider()

        # =====================================================
        # ENGINE TEMPORAL
        # =====================================================

        render_filtro_periodo()

        st.divider()

        st.subheader("Navegação")

        # =====================================================
        # MENU MASTER
        # =====================================================

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

        # =====================================================
        # MENU OPERADOR
        # =====================================================

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

        # =====================================================
        # LOGOUT
        # =====================================================

        if st.button("🚪 SAIR DO SISTEMA"):

            if "audit_logs" not in st.session_state:

                st.session_state.audit_logs = []

            st.session_state.audit_logs.append({

                "timestamp": "Logout",

                "usuario": st.session_state.user_name,

                "role": role,

                "acao": "LOGOUT",

                "detalhes": "Usuário saiu do sistema"
            })

            st.session_state.clear()

            st.rerun()

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown("""
    <div class="status">
    🟢 Sistema Operacional
    </div>

    <div class="status">
    🔒 Segurança Ativa
    </div>

    <div class="status">
    ⚡ Ambiente Enterprise
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
    rastreabilidade e inteligência operacional
    aplicada à engenharia industrial.
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # RENDERIZAÇÃO DAS PÁGINAS
    # =====================================================

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