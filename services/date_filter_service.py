from datetime import datetime, timedelta
import streamlit as st


# =========================================================
# ENGINE TEMPORAL GLOBAL
# =========================================================

def inicializar_periodo():

    hoje = datetime.now().date()

    if "data_inicio" not in st.session_state:

        st.session_state.data_inicio = hoje

    if "data_fim" not in st.session_state:

        st.session_state.data_fim = hoje

    if "periodo_label" not in st.session_state:

        st.session_state.periodo_label = "Hoje"


# =========================================================
# FILTRO SIDEBAR
# =========================================================

def render_filtro_periodo():

    st.sidebar.markdown("## 📅 Período Analítico")

    opcao = st.sidebar.selectbox(

        "Selecionar período",

        [

            "Hoje",

            "Últimos 7 dias",

            "Últimos 30 dias",

            "Personalizado"
        ]
    )

    hoje = datetime.now().date()

    if opcao == "Hoje":

        data_inicio = hoje
        data_fim = hoje

    elif opcao == "Últimos 7 dias":

        data_inicio = hoje - timedelta(days=7)
        data_fim = hoje

    elif opcao == "Últimos 30 dias":

        data_inicio = hoje - timedelta(days=30)
        data_fim = hoje

    else:

        col1, col2 = st.sidebar.columns(2)

        with col1:

            data_inicio = st.date_input(

                "Início",

                value=hoje
            )

        with col2:

            data_fim = st.date_input(

                "Fim",

                value=hoje
            )

    st.session_state.data_inicio = data_inicio

    st.session_state.data_fim = data_fim

    st.session_state.periodo_label = opcao


# =========================================================
# FILTRAR COLETAS
# =========================================================

def filtrar_coletas(coletas):

    data_inicio = st.session_state.data_inicio

    data_fim = st.session_state.data_fim

    resultado = []

    for coleta in coletas:

        try:

            data_coleta = datetime.strptime(

                coleta["data_coleta"],
                "%Y-%m-%d"
            ).date()

            if data_inicio <= data_coleta <= data_fim:

                resultado.append(coleta)

        except:

            pass

    return resultado