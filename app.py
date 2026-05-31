"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    INDUSTRIAL CONTROL PLATFORM v2.0                         ║
║                                                                              ║
║  Desenvolvido com padrões ISA-101 (High-Performance HMI)                    ║
║  Refatoração Completa: Código Limpo • Design Premium • Zero Duplicatas      ║
║                                                                              ║
║  Princípios Aplicados:                                                       ║
║  ✓ Paleta de cores neutra (cinzas) para reduzir fadiga cognitiva            ║
║  ✓ Cores vibrantes reservadas apenas para alarmes/anomalias                 ║
║  ✓ Componentes padronizados e reutilizáveis                                 ║
║  ✓ Eliminação total de código duplicado                                     ║
║  ✓ Remoção da faixa branca no topo                                          ║
║  ✓ Navegação inteligente baseada em roles                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from dataclasses import dataclass
from typing import Callable, List, Dict, Optional
from enum import Enum

# =========================================================
# IMPORTS ORIGINAIS (Manter compatibilidade)
# =========================================================
try:
    from pages.login import show_login
    from pages.dashboard import show_dashboard
    from pages.parameters import show_parameters
    from pages.collection_points import show_collection_points
    from pages.new_collection import show_new_collection
    from pages.history import show_history
    from pages.audit import show_audit
    from pages.manager_dashboard import show_manager_dashboard
    from pages.corporate_registry import show_corporate_registry
    from pages.user_management import show_user_management
    from pages.trend_analysis import show_trend_analysis
    from services.date_filter_service import inicializar_periodo, render_filtro_periodo
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False

# =========================================================
# ENUMS & DATA CLASSES
# =========================================================
class UserRole(str, Enum):
    MASTER = "master"
    OPERADOR = "operador"

@dataclass
class PageConfig:
    key: str
    label: str
    icon: str
    func: Callable
    roles: List[UserRole]

# =========================================================
# DESIGN SYSTEM ISA-101
# =========================================================
class ISA101ColorPalette:
    """Paleta de cores baseada em ISA-101 para HMI de alto desempenho"""
    
    # Backgrounds
    BG_MAIN = "#0F0F0F"
    BG_CARD = "#1A1A1A"
    BG_SIDEBAR = "#141414"
    
    # Borders & Dividers
    BORDER_PRIMARY = "#2A2A2A"
    BORDER_HOVER = "#3A3A3A"
    
    # Text
    TEXT_PRIMARY = "#E8E8E8"
    TEXT_SECONDARY = "#B0B0B0"
    TEXT_MUTED = "#808080"
    
    # Functional Colors (ISA-101 compliant)
    ACCENT_BLUE = "#4A90E2"
    SUCCESS_GREEN = "#2D7D46"
    WARNING_AMBER = "#D97706"
    DANGER_RED = "#DC2626"
    INFO_CYAN = "#0891B2"

def apply_isa101_styling():
    """
    Aplica o design system ISA-101 completo.
    Inclui: remoção de faixa branca, padronização de componentes,
    paleta de cores de alto desempenho e tipografia profissional.
    """
    st.markdown(f"""
    <style>
        /* ========== VARIÁVEIS CSS ========== */
        :root {{
            --isa-bg-main: {ISA101ColorPalette.BG_MAIN};
            --isa-bg-card: {ISA101ColorPalette.BG_CARD};
            --isa-bg-sidebar: {ISA101ColorPalette.BG_SIDEBAR};
            --isa-border: {ISA101ColorPalette.BORDER_PRIMARY};
            --isa-border-hover: {ISA101ColorPalette.BORDER_HOVER};
            --isa-text-primary: {ISA101ColorPalette.TEXT_PRIMARY};
            --isa-text-secondary: {ISA101ColorPalette.TEXT_SECONDARY};
            --isa-text-muted: {ISA101ColorPalette.TEXT_MUTED};
            --isa-accent: {ISA101ColorPalette.ACCENT_BLUE};
            --isa-success: {ISA101ColorPalette.SUCCESS_GREEN};
            --isa-warning: {ISA101ColorPalette.WARNING_AMBER};
            --isa-danger: {ISA101ColorPalette.DANGER_RED};
        }}

        /* ========== REMOVE WHITE STRIP AT TOP ========== */
        header[data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0) !important;
            height: 0px !important;
            display: none !important;
        }}
        
        .block-container {{
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
        }}

        /* ========== GLOBAL STYLES ========== */
        .stApp {{
            background-color: var(--isa-bg-main);
            color: var(--isa-text-primary);
        }}

        html, body {{
            font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--isa-bg-main);
            color: var(--isa-text-primary);
        }}

        /* ========== SIDEBAR STYLING ========== */
        [data-testid="stSidebar"] {{
            background-color: var(--isa-bg-sidebar);
            border-right: 1px solid var(--isa-border);
        }}
        
        [data-testid="stSidebarNav"] {{ 
            display: none; 
        }}

        /* ========== UNIFIED BUTTON STYLING ========== */
        .stButton > button {{
            width: 100% !important;
            border-radius: 6px !important;
            border: 1px solid var(--isa-border) !important;
            background-color: var(--isa-bg-card) !important;
            color: var(--isa-text-primary) !important;
            padding: 0.6rem 1rem !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            transition: all 0.2s ease-in-out !important;
            text-align: left !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            margin-bottom: 8px !important;
        }}

        .stButton > button:hover {{
            border-color: var(--isa-accent) !important;
            background-color: var(--isa-border-hover) !important;
            transform: translateX(2px) !important;
            box-shadow: 0 2px 8px rgba(74, 144, 226, 0.15) !important;
        }}

        .stButton > button:active {{
            background-color: var(--isa-accent) !important;
            color: white !important;
            border-color: var(--isa-accent) !important;
        }}

        /* ========== ACTIVE PAGE INDICATOR ========== */
        .stButton > button[aria-pressed="true"] {{
            border-left: 4px solid var(--isa-accent) !important;
            background-color: var(--isa-border-hover) !important;
            padding-left: calc(1rem - 4px) !important;
        }}

        /* ========== INPUTS & SELECTS ========== */
        div[data-baseweb="select"], 
        .stTextInput input, 
        .stTextArea textarea,
        .stNumberInput input {{
            background-color: var(--isa-bg-card) !important;
            border: 1px solid var(--isa-border) !important;
            border-radius: 6px !important;
            color: var(--isa-text-primary) !important;
            padding: 0.6rem 0.8rem !important;
            transition: all 0.2s ease-in-out !important;
        }}

        div[data-baseweb="select"]:hover,
        .stTextInput input:hover,
        .stTextArea textarea:hover,
        .stNumberInput input:hover {{
            border-color: var(--isa-border-hover) !important;
        }}

        div[data-baseweb="select"]:focus-within,
        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {{
            border-color: var(--isa-accent) !important;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1) !important;
        }}

        /* ========== MULTISELECT TAGS ========== */
        span[data-baseweb="tag"] {{
            background-color: var(--isa-accent) !important;
            color: white !important;
            border-radius: 4px !important;
            padding: 4px 8px !important;
        }}

        /* ========== SELECT DROPDOWN ========== */
        [data-baseweb="select"] > div {{
            background-color: var(--isa-bg-card) !important;
            color: var(--isa-text-primary) !important;
        }}

        [data-baseweb="popover"] {{
            background-color: var(--isa-bg-card) !important;
        }}

        ul[role="listbox"] {{
            background-color: var(--isa-bg-card) !important;
            border: 1px solid var(--isa-border) !important;
        }}

        ul[role="listbox"] li {{
            background-color: var(--isa-bg-card) !important;
            color: var(--isa-text-primary) !important;
            transition: background-color 0.1s ease !important;
        }}

        ul[role="listbox"] li:hover {{
            background-color: var(--isa-border-hover) !important;
        }}

        /* ========== LABELS ========== */
        label, [data-testid="stWidgetLabel"] {{
            color: var(--isa-text-secondary) !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            opacity: 1 !important;
        }}

        /* ========== METRICS ========== */
        div[data-testid="metric-container"] {{
            background-color: var(--isa-bg-card) !important;
            border: 1px solid var(--isa-border) !important;
            padding: 15px !important;
            border-radius: 8px !important;
        }}

        /* ========== TABS ========== */
        button[data-baseweb="tab"] {{
            color: var(--isa-text-secondary) !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.2s ease !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: var(--isa-accent) !important;
            border-bottom-color: var(--isa-accent) !important;
        }}

        /* ========== TABLES ========== */
        table {{
            background-color: var(--isa-bg-card) !important;
            color: var(--isa-text-primary) !important;
        }}

        thead {{
            background-color: var(--isa-border-hover) !important;
        }}

        tbody tr:hover {{
            background-color: var(--isa-border-hover) !important;
        }}

        /* ========== ALERTS ========== */
        .stAlert {{
            color: var(--isa-text-primary) !important;
            border-radius: 6px !important;
        }}

        .stAlert > div {{
            background-color: var(--isa-bg-card) !important;
        }}

        /* ========== DISABLED FIELDS ========== */
        input:disabled, textarea:disabled {{
            color: var(--isa-text-muted) !important;
            -webkit-text-fill-color: var(--isa-text-muted) !important;
            opacity: 1 !important;
        }}

        /* ========== CARDS & CONTAINERS ========== */
        .isa-card {{
            background-color: var(--isa-bg-card);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--isa-border);
            margin-bottom: 20px;
        }}

        /* ========== TYPOGRAPHY ========== */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--isa-text-primary) !important;
            font-weight: 600 !important;
        }}

        .isa-header-main {{
            font-size: 24px;
            font-weight: 700;
            color: var(--isa-text-primary);
            margin-bottom: 5px;
        }}

        .isa-header-sub {{
            font-size: 14px;
            color: var(--isa-text-secondary);
            margin-bottom: 20px;
        }}

        /* ========== STATUS BADGES ========== */
        .status-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
            border: 1px solid;
        }}

        .status-online {{
            background: rgba(45, 125, 70, 0.15);
            color: #4ADE80;
            border-color: var(--isa-success);
        }}

        .status-warning {{
            background: rgba(217, 119, 6, 0.15);
            color: var(--isa-warning);
            border-color: var(--isa-warning);
        }}

        .status-error {{
            background: rgba(220, 38, 38, 0.15);
            color: var(--isa-danger);
            border-color: var(--isa-danger);
        }}

        /* ========== DIVIDER ========== */
        hr {{
            border: none;
            border-top: 1px solid var(--isa-border);
            margin: 15px 0;
        }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# COMPONENT UTILITIES
# =========================================================
def render_nav_button(label: str, icon: str, page_key: str) -> bool:
    """
    Renderiza um botão de navegação com indicador de página ativa.
    
    Args:
        label: Texto do botão
        icon: Emoji ou ícone
        page_key: Chave da página no session_state
        
    Returns:
        True se o botão foi clicado
    """
    is_active = st.session_state.current_page == page_key
    button_key = f"nav_btn_{page_key}"
    
    if st.button(f"{icon} {label}", key=button_key, use_container_width=True):
        st.session_state.current_page = page_key
        st.rerun()
    
    return is_active

def render_header(title: str, subtitle: str, status_items: Optional[List[tuple]] = None):
    """
    Renderiza o cabeçalho principal com título, subtítulo e status badges.
    
    Args:
        title: Título principal
        subtitle: Subtítulo/descrição
        status_items: Lista de tuplas (label, status_type) para badges
    """
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"<div class='isa-header-main'>{title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='isa-header-sub'>{subtitle}</div>", unsafe_allow_html=True)
    
    if status_items:
        with col2:
            status_html = ""
            for label, status_type in status_items:
                status_html += f'<div class="status-badge status-{status_type}">{label}</div>'
            st.markdown(f"<div style='display: flex; justify-content: flex-end;'>{status_html}</div>", unsafe_allow_html=True)

def render_sidebar_navigation(pages: Dict[str, PageConfig], role: UserRole):
    """
    Renderiza a navegação da sidebar de forma centralizada.
    
    Args:
        pages: Dicionário de páginas disponíveis
        role: Role do usuário (master ou operador)
    """
    for key, page in pages.items():
        if role in page.roles:
            render_nav_button(page.label, page.icon, page.key)

def render_user_status(user_name: str, role: str):
    """Renderiza o status do usuário na sidebar"""
    st.markdown(f"""
    <div style="
        background: rgba(45, 125, 70, 0.1);
        border: 1px solid var(--isa-success);
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 15px;
    ">
        <div style="font-size: 12px; color: var(--isa-text-secondary); margin-bottom: 4px;">USUÁRIO ATIVO</div>
        <div style="font-weight: 600; color: var(--isa-text-primary);">{user_name}</div>
        <div style="font-size: 11px; color: var(--isa-text-muted); margin-top: 4px;">Role: {role.upper()}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Industrial Control | ISA-101",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# APPLY STYLING
# =========================================================
apply_isa101_styling()

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
def initialize_session_state():
    """Inicializa todas as variáveis de sessão necessárias"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = "Usuário"
    
    if "role" not in st.session_state:
        st.session_state.role = UserRole.OPERADOR

initialize_session_state()

# =========================================================
# PAGE DEFINITIONS
# =========================================================
def create_pages_config() -> Dict[str, PageConfig]:
    """
    Define todas as páginas disponíveis no sistema.
    Centraliza a configuração para evitar duplicatas.
    """
    
    # Funções mock para quando os imports não estão disponíveis
    def mock_page(name):
        st.markdown(f"<div class='isa-card'><h2>{name}</h2><p>Página em desenvolvimento...</p></div>", unsafe_allow_html=True)
    
    # Mapear funções reais ou mocks
    dashboard_func = show_dashboard if IMPORTS_AVAILABLE else lambda: mock_page("Dashboard")
    parameters_func = show_parameters if IMPORTS_AVAILABLE else lambda: mock_page("Parâmetros")
    collection_points_func = show_collection_points if IMPORTS_AVAILABLE else lambda: mock_page("Pontos de Coleta")
    new_collection_func = show_new_collection if IMPORTS_AVAILABLE else lambda: mock_page("Nova Coleta")
    history_func = show_history if IMPORTS_AVAILABLE else lambda: mock_page("Histórico")
    audit_func = show_audit if IMPORTS_AVAILABLE else lambda: mock_page("Auditoria")
    manager_dashboard_func = show_manager_dashboard if IMPORTS_AVAILABLE else lambda: mock_page("Dashboard Gerencial")
    corporate_registry_func = show_corporate_registry if IMPORTS_AVAILABLE else lambda: mock_page("Cadastros Corporativos")
    user_management_func = show_user_management if IMPORTS_AVAILABLE else lambda: mock_page("Gestão de Usuários")
    trend_analysis_func = show_trend_analysis if IMPORTS_AVAILABLE else lambda: mock_page("Trend Analysis")
    
    return {
        "dashboard": PageConfig(
            key="dashboard",
            label="Dashboard",
            icon="📊",
            func=dashboard_func,
            roles=[UserRole.MASTER, UserRole.OPERADOR]
        ),
        "manager_dashboard": PageConfig(
            key="manager_dashboard",
            label="Dashboard Gerencial",
            icon="📈",
            func=manager_dashboard_func,
            roles=[UserRole.MASTER, UserRole.OPERADOR]
        ),
        "parameters": PageConfig(
            key="parameters",
            label="Parâmetros",
            icon="🧪",
            func=parameters_func,
            roles=[UserRole.MASTER]
        ),
        "collection_points": PageConfig(
            key="collection_points",
            label="Pontos de Coleta",
            icon="📍",
            func=collection_points_func,
            roles=[UserRole.MASTER]
        ),
        "new_collection": PageConfig(
            key="new_collection",
            label="Nova Coleta",
            icon="🧫",
            func=new_collection_func,
            roles=[UserRole.MASTER, UserRole.OPERADOR]
        ),
        "history": PageConfig(
            key="history",
            label="Histórico",
            icon="📚",
            func=history_func,
            roles=[UserRole.MASTER, UserRole.OPERADOR]
        ),
        "trend_analysis": PageConfig(
            key="trend_analysis",
            label="Trend Analysis",
            icon="📈",
            func=trend_analysis_func,
            roles=[UserRole.MASTER, UserRole.OPERADOR]
        ),
        "audit": PageConfig(
            key="audit",
            label="Auditoria",
            icon="📜",
            func=audit_func,
            roles=[UserRole.MASTER]
        ),
        "corporate_registry": PageConfig(
            key="corporate_registry",
            label="Cadastros Corporativos",
            icon="⚙️",
            func=corporate_registry_func,
            roles=[UserRole.MASTER]
        ),
        "user_management": PageConfig(
            key="user_management",
            label="Gestão de Usuários",
            icon="👥",
            func=user_management_func,
            roles=[UserRole.MASTER]
        ),
    }

# =========================================================
# MAIN APPLICATION
# =========================================================
def main():
    """Função principal da aplicação"""
    
    # Verificar autenticação
    if not st.session_state.logged_in:
        if IMPORTS_AVAILABLE:
            show_login()
        else:
            st.error("Sistema de login não disponível. Verifique os imports.")
        st.stop()
    
    # Inicializar período temporal (se disponível)
    if IMPORTS_AVAILABLE:
        try:
            inicializar_periodo()
        except Exception as e:
            st.warning(f"Aviso: Serviço de período não disponível ({e})")
    
    # Obter configuração de páginas
    pages = create_pages_config()
    role = UserRole(st.session_state.get("role", UserRole.OPERADOR.value))
    
    # SIDEBAR
    with st.sidebar:
        st.markdown("<h1 style='font-size: 20px; margin-bottom: 10px;'>🏭 Industrial Control</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--isa-text-secondary); font-size: 12px; margin-bottom: 15px;'>Plataforma ISA-101</p>", unsafe_allow_html=True)
        st.divider()
        
        # Status do usuário
        render_user_status(st.session_state.user_name, role.value)
        
        # Filtro de período (se disponível)
        if IMPORTS_AVAILABLE:
            try:
                render_filtro_periodo()
                st.divider()
            except Exception:
                pass
        
        # Navegação
        st.subheader("Navegação")
        render_sidebar_navigation(pages, role)
        
        st.divider()
        
        # Botão de logout
        if st.button("🚪 Sair do Sistema", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # MAIN CONTENT AREA
    render_header(
        title="Controle Analítico Industrial",
        subtitle="Monitoramento em tempo real • Padrão ISA-101 • High-Performance HMI",
        status_items=[
            ("🟢 SISTEMA OPERACIONAL", "online"),
            ("🔒 SEGURANÇA ATIVA", "online"),
        ]
    )
    
    st.divider()
    
    # Renderizar página selecionada
    current_page_key = st.session_state.current_page
    if current_page_key in pages:
        pages[current_page_key].func()
    else:
        st.error(f"Página '{current_page_key}' não encontrada.")

# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    main()
