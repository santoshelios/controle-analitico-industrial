<<<<<<< HEAD
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
# CSS GLOBAL ISA-101 LIGHT / MEDIUM
# =========================================================

st.markdown("""

<style>

/* =========================================================
APP
========================================================= */

.stApp {

    background:
        #1E1E1E;

    color:
        #D9D9D9;
}

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {

    font-family:
        "Inter",
        sans-serif;

    color:
        #D9D9D9;
}

/* =========================================================
SIDEBAR
========================================================= */

[data-testid="stSidebar"] {

    width:
        330px !important;

    background:
        #252526;

    border-right:
        1px solid #3A3A3A;

    box-shadow:
        none;
}

/* REMOVE NAV */

[data-testid="stSidebarNav"] {

    display: none;
}

/* TEXT */

[data-testid="stSidebar"] * {

    color:
        #D9D9D9;
}

/* =========================================================
SIDEBAR BUTTONS
========================================================= */

[data-testid="stSidebar"] .stButton {

    display:
        flex;

    justify-content:
        center;
}

[data-testid="stSidebar"] .stButton > button {

    width:
        260px !important;

    min-width:
        260px !important;

    max-width:
        260px !important;

    height:
        54px;

    margin-bottom:
        10px;

    border-radius:
        10px;

    border:
        1px solid #3A3A3A;

    background:
        #2D2D30 !important;

    color:
        #D9D9D9 !important;

    font-weight:
        600;

    font-size:
        14px;

    text-align:
        left;

    padding-left:
        18px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        flex-start;

    transition:
        all 0.2s ease;

    box-shadow:
        none;
}

[data-testid="stSidebar"] .stButton > button:hover {

    background:
        #3A3A3A !important;

    border:
        1px solid #5A5A5A;

    color:
        white !important;

    transform:
        translateX(4px);
}

/* FORCE BUTTON CONTENT */

[data-testid="stSidebar"] .stButton > button p {

    width:
        100% !important;

    text-align:
        left !important;

    margin:
        0 !important;
}

/* =========================================================
USER BLOCK
========================================================= */

[data-testid="stSidebar"] .stAlert {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;
}

/* =========================================================
LABELS
========================================================= */

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stCheckbox label,
.stTextArea label {

    color:
        #D9D9D9 !important;

    font-weight:
        600 !important;

    font-size:
        13px !important;
}

/* =========================================================
INPUTS
========================================================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        8px !important;

    color:
        #D9D9D9 !important;
}

.stSelectbox div[data-baseweb="select"] > div {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        8px !important;

    color:
        #D9D9D9 !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {

    width:
        100%;

    height:
        50px;

    border-radius:
        10px;

    border:
        1px solid #3A3A3A;

    background:
        #2D2D30 !important;

    color:
        #D9D9D9 !important;

    font-weight:
        600;

    font-size:
        14px;

    transition:
        all 0.2s ease;

    box-shadow:
        none;
}

.stButton > button:hover {

    background:
        #3A3A3A !important;

    border:
        1px solid #5A5A5A;

    color:
        white !important;
}

/* =========================================================
FORM BUTTONS
========================================================= */

.stForm button {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;

    color:
        #D9D9D9 !important;

    font-weight:
        600 !important;

    box-shadow:
        none !important;
}

.stForm button:hover {

    background:
        #3A3A3A !important;

    border:
        1px solid #5A5A5A !important;
}

/* =========================================================
METRICS / KPI - ISA FINAL
========================================================= */

div[data-testid="metric-container"] {

    position:
        relative;

    overflow:
        hidden;

    background:
        #252526 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;

    padding:
        20px !important;

    box-shadow:
        none !important;

    transition:
        all 0.2s ease;
}

/* REMOVE HERANÇA ANTIGA */

div[data-testid="metric-container"]::before,
div[data-testid="metric-container"]::after {

    display:
        none !important;

    content:
        none !important;
}

/* HOVER */

div[data-testid="metric-container"]:hover {

    background:
        #2D2D30 !important;

    border:
        1px solid #5A5A5A !important;

    transform:
        translateY(-2px);
}

/* LABEL */

div[data-testid="metric-container"] label {

    color:
        #A0A0A0 !important;

    font-size:
        13px !important;

    font-weight:
        700 !important;

    letter-spacing:
        0.3px;
}

/* VALUE */

div[data-testid="stMetricValue"] {

    color:
        #F2F2F2 !important;

    font-size:
        36px !important;

    font-weight:
        800 !important;

    text-shadow:
        none !important;
}

/* DELTA */

div[data-testid="stMetricDelta"] {

    font-size:
        12px !important;

    font-weight:
        700 !important;
}

/* =========================================================
STATUS
========================================================= */

.status {

    display:
        inline-block;

    padding:
        8px 14px;

    margin-right:
        10px;

    margin-bottom:
        12px;

    border-radius:
        8px;

    background:
        #2D2D30;

    border:
        1px solid #3A3A3A;

    color:
        #BFBFBF;

    font-size:
        12px;

    font-weight:
        600;
}

/* =========================================================
TABLES
========================================================= */

table {

    width:
        100% !important;

    border-collapse:
        collapse !important;

    background:
        #252526 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;

    overflow:
        hidden !important;

    color:
        #D9D9D9 !important;
}

/* HEADERS */

table thead tr th,
div[data-testid="stDataFrame"] thead tr th {

    background:
        #2D2D30 !important;

    color:
        #D9D9D9 !important;

    font-weight:
        700 !important;

    border:
        none !important;

    padding:
        14px !important;
}

/* ROWS */

table tbody tr,
div[data-testid="stDataFrame"] tbody tr {

    background:
        #252526 !important;

    color:
        #D9D9D9 !important;

    transition:
        all 0.2s ease;
}

/* ZEBRA */

table tbody tr:nth-child(even),
div[data-testid="stDataFrame"] tbody tr:nth-child(even) {

    background:
        #2B2B2B !important;
}

/* HOVER */

table tbody tr:hover,
div[data-testid="stDataFrame"] tbody tr:hover {

    background:
        #333333 !important;
}

/* CELLS */

table td,
div[data-testid="stDataFrame"] td {

    border:
        none !important;

    padding:
        12px !important;

    font-size:
        13px !important;
}

/* =========================================================
TÍTULOS
========================================================= */

.main-title {

    font-size:
        48px;

    font-weight:
        800;

    color:
        #F2F2F2;

    margin-top:
        10px;

    margin-bottom:
        12px;
}

.main-subtitle {

    font-size:
        17px;

    color:
        #A0A0A0;

    line-height:
        1.7;

    max-width:
        900px;

    margin-bottom:
        36px;
}

/* =========================================================
PLOTLY
========================================================= */

.js-plotly-plot {

    border:
        1px solid #3A3A3A;

    border-radius:
        12px;

    background:
        #252526;
}

/* =========================================================
SCROLLBAR
========================================================= */

::-webkit-scrollbar {

    width:
        10px;
}

::-webkit-scrollbar-track {

    background:
        #1E1E1E;
}

::-webkit-scrollbar-thumb {

    background:
        #444;

    border-radius:
        10px;
}

::-webkit-scrollbar-thumb:hover {

    background:
        #666;
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

        Industrial Analytics Platform

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

=======
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
# CSS GLOBAL ISA-101 LIGHT / MEDIUM
# =========================================================

st.markdown("""

<style>

/* =========================================================
APP
========================================================= */

.stApp {

    background:
        #1E1E1E;

    color:
        #D9D9D9;
}

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {

    font-family:
        "Inter",
        sans-serif;

    color:
        #D9D9D9;
}

/* =========================================================
SIDEBAR
========================================================= */

[data-testid="stSidebar"] {

    width:
        330px !important;

    background:
        #252526;

    border-right:
        1px solid #3A3A3A;

    box-shadow:
        none;
}

/* REMOVE NAV */

[data-testid="stSidebarNav"] {

    display: none;
}

/* TEXT */

[data-testid="stSidebar"] * {

    color:
        #D9D9D9;
}

/* =========================================================
SIDEBAR BUTTONS
========================================================= */

[data-testid="stSidebar"] .stButton {

    display:
        flex;

    justify-content:
        center;
}

[data-testid="stSidebar"] .stButton > button {

    width:
        260px !important;

    min-width:
        260px !important;

    max-width:
        260px !important;

    height:
        54px;

    margin-bottom:
        10px;

    border-radius:
        10px;

    border:
        1px solid #3A3A3A;

    background:
        #2D2D30 !important;

    color:
        #D9D9D9 !important;

    font-weight:
        600;

    font-size:
        14px;

    text-align:
        left;

    padding-left:
        18px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        flex-start;

    transition:
        all 0.2s ease;

    box-shadow:
        none;
}

[data-testid="stSidebar"] .stButton > button:hover {

    background:
        #3A3A3A !important;

    border:
        1px solid #5A5A5A;

    color:
        white !important;

    transform:
        translateX(4px);
}

/* FORCE BUTTON CONTENT */

[data-testid="stSidebar"] .stButton > button p {

    width:
        100% !important;

    text-align:
        left !important;

    margin:
        0 !important;
}

/* =========================================================
USER BLOCK
========================================================= */

[data-testid="stSidebar"] .stAlert {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;
}

/* =========================================================
LABELS
========================================================= */

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stCheckbox label,
.stTextArea label {

    color:
        #D9D9D9 !important;

    font-weight:
        600 !important;

    font-size:
        13px !important;
}

/* =========================================================
INPUTS
========================================================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        8px !important;

    color:
        #D9D9D9 !important;
}

.stSelectbox div[data-baseweb="select"] > div {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        8px !important;

    color:
        #D9D9D9 !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {

    width:
        100%;

    height:
        50px;

    border-radius:
        10px;

    border:
        1px solid #3A3A3A;

    background:
        #2D2D30 !important;

    color:
        #D9D9D9 !important;

    font-weight:
        600;

    font-size:
        14px;

    transition:
        all 0.2s ease;

    box-shadow:
        none;
}

.stButton > button:hover {

    background:
        #3A3A3A !important;

    border:
        1px solid #5A5A5A;

    color:
        white !important;
}

/* =========================================================
FORM BUTTONS
========================================================= */

.stForm button {

    background:
        #2D2D30 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;

    color:
        #D9D9D9 !important;

    font-weight:
        600 !important;

    box-shadow:
        none !important;
}

.stForm button:hover {

    background:
        #3A3A3A !important;

    border:
        1px solid #5A5A5A !important;
}

/* =========================================================
METRICS / KPI - ISA FINAL
========================================================= */

div[data-testid="metric-container"] {

    position:
        relative;

    overflow:
        hidden;

    background:
        #252526 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;

    padding:
        20px !important;

    box-shadow:
        none !important;

    transition:
        all 0.2s ease;
}

/* REMOVE HERANÇA ANTIGA */

div[data-testid="metric-container"]::before,
div[data-testid="metric-container"]::after {

    display:
        none !important;

    content:
        none !important;
}

/* HOVER */

div[data-testid="metric-container"]:hover {

    background:
        #2D2D30 !important;

    border:
        1px solid #5A5A5A !important;

    transform:
        translateY(-2px);
}

/* LABEL */

div[data-testid="metric-container"] label {

    color:
        #A0A0A0 !important;

    font-size:
        13px !important;

    font-weight:
        700 !important;

    letter-spacing:
        0.3px;
}

/* VALUE */

div[data-testid="stMetricValue"] {

    color:
        #F2F2F2 !important;

    font-size:
        36px !important;

    font-weight:
        800 !important;

    text-shadow:
        none !important;
}

/* DELTA */

div[data-testid="stMetricDelta"] {

    font-size:
        12px !important;

    font-weight:
        700 !important;
}

/* =========================================================
STATUS
========================================================= */

.status {

    display:
        inline-block;

    padding:
        8px 14px;

    margin-right:
        10px;

    margin-bottom:
        12px;

    border-radius:
        8px;

    background:
        #2D2D30;

    border:
        1px solid #3A3A3A;

    color:
        #BFBFBF;

    font-size:
        12px;

    font-weight:
        600;
}

/* =========================================================
TABLES
========================================================= */

table {

    width:
        100% !important;

    border-collapse:
        collapse !important;

    background:
        #252526 !important;

    border:
        1px solid #3A3A3A !important;

    border-radius:
        10px !important;

    overflow:
        hidden !important;

    color:
        #D9D9D9 !important;
}

/* HEADERS */

table thead tr th,
div[data-testid="stDataFrame"] thead tr th {

    background:
        #2D2D30 !important;

    color:
        #D9D9D9 !important;

    font-weight:
        700 !important;

    border:
        none !important;

    padding:
        14px !important;
}

/* ROWS */

table tbody tr,
div[data-testid="stDataFrame"] tbody tr {

    background:
        #252526 !important;

    color:
        #D9D9D9 !important;

    transition:
        all 0.2s ease;
}

/* ZEBRA */

table tbody tr:nth-child(even),
div[data-testid="stDataFrame"] tbody tr:nth-child(even) {

    background:
        #2B2B2B !important;
}

/* HOVER */

table tbody tr:hover,
div[data-testid="stDataFrame"] tbody tr:hover {

    background:
        #333333 !important;
}

/* CELLS */

table td,
div[data-testid="stDataFrame"] td {

    border:
        none !important;

    padding:
        12px !important;

    font-size:
        13px !important;
}

/* =========================================================
TÍTULOS
========================================================= */

.main-title {

    font-size:
        48px;

    font-weight:
        800;

    color:
        #F2F2F2;

    margin-top:
        10px;

    margin-bottom:
        12px;
}

.main-subtitle {

    font-size:
        17px;

    color:
        #A0A0A0;

    line-height:
        1.7;

    max-width:
        900px;

    margin-bottom:
        36px;
}

/* =========================================================
PLOTLY
========================================================= */

.js-plotly-plot {

    border:
        1px solid #3A3A3A;

    border-radius:
        12px;

    background:
        #252526;
}

/* =========================================================
SCROLLBAR
========================================================= */

::-webkit-scrollbar {

    width:
        10px;
}

::-webkit-scrollbar-track {

    background:
        #1E1E1E;
}

::-webkit-scrollbar-thumb {

    background:
        #444;

    border-radius:
        10px;
}

::-webkit-scrollbar-thumb:hover {

    background:
        #666;
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

        Industrial Analytics Platform

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

>>>>>>> 6ed7a27 (Refinamento visual ISA industrial)
        show_trend_analysis()