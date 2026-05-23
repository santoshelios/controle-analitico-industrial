import streamlit as st
from datetime import datetime

from services.audit_service import registrar_auditoria

from validation_engine import validar_parametro

import json

from db_connection import get_safe_connection

# =========================================================
# NEW COLLECTION PAGE
# =========================================================

def show_new_collection():

    st.title("🧫 Nova Coleta")

    st.markdown("""
    Registro operacional das análises industriais
    realizadas nos pontos monitorados.
    """)

    st.divider()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "coletas" not in st.session_state:

        st.session_state.coletas = []

    # =====================================================
    # LOAD POSTGRESQL
    # =====================================================

    conn = get_safe_connection()

    cursor = conn.cursor()

    # =====================================================
    # PONTOS DE COLETA
    # =====================================================

    cursor.execute("""

        SELECT

            nome,
            planta,
            setor,
            parametros

        FROM collection_points

        WHERE status = 'Ativo'

        ORDER BY nome

    """)

    pontos_db = cursor.fetchall()

    if not pontos_db:

        st.warning(
            "Nenhum ponto de coleta cadastrado."
        )

        return

    pontos = []

    for row in pontos_db:

        pontos.append({

            "nome": row[0],

            "planta": row[1],

            "setor": row[2],

            "parametros": row[3] if row[3] else []
        })

    # =====================================================
    # PARÂMETROS
    # =====================================================

    cursor.execute("""

        SELECT

            nome,
            limite_min,
            limite_max

        FROM parameters

        ORDER BY nome

    """)

    parametros_db = cursor.fetchall()

    parametros_cadastrados = []

    for row in parametros_db:

        parametros_cadastrados.append({

            "nome": row[0],

            "limite_min": row[1],

            "limite_max": row[2]
        })

    cursor.close()

    nomes_pontos = [

        item["nome"]

        for item in pontos
    ]

    # =====================================================
    # SELEÇÃO DO PONTO
    # =====================================================

    st.subheader("🏭 Informações da Coleta")

    ponto = st.selectbox(

        "Ponto de Coleta",

        nomes_pontos
    )

    # =====================================================
    # BUSCA PONTO
    # =====================================================

    ponto_selecionado = next(

        (
            item for item in pontos
            if item["nome"] == ponto
        ),

        None
    )

    planta = ""
    setor = ""
    parametros = []

    if ponto_selecionado:

        planta = ponto_selecionado["planta"]

        setor = ponto_selecionado["setor"]

        parametros = ponto_selecionado["parametros"]

    # =====================================================
    # FORMULÁRIO
    # =====================================================

    with st.form("form_collection"):

        col1, col2 = st.columns(2)

        # =================================================
        # COLUNA 1
        # =================================================

        with col1:

            st.text_input(

                "Planta",

                value=planta,

                disabled=True
            )

            st.text_input(

                "Setor",

                value=setor,

                disabled=True
            )

        # =================================================
        # COLUNA 2
        # =================================================

        with col2:

            operador = st.text_input(

                "Operador / Analista",

                value=st.session_state.user_name,

                disabled=True
            )

            data_coleta = st.date_input(
                "Data da Coleta"
            )

            hora_coleta = st.time_input(
                "Hora da Coleta"
            )

        st.divider()

        # =================================================
        # RESULTADOS ANALÍTICOS
        # =================================================

        st.subheader("🧪 Resultados Analíticos")

        resultados = {}

        if parametros:

            for parametro in parametros:

                resultados[parametro] = st.text_input(
                    parametro
                )

        else:

            st.warning(
                "Nenhum parâmetro vinculado ao ponto."
            )

        st.divider()

        observacoes = st.text_area(

            "Observações Operacionais",

            height=120
        )

        salvar = st.form_submit_button(
            "Salvar Coleta"
        )

        # =================================================
        # SALVAR
        # =================================================

        if salvar:

            resultados_processados = {}

            total_alertas = 0

            # =============================================
            # PROCESSAMENTO ANALÍTICO
            # =============================================

            for parametro, valor in resultados.items():

                limite_min_valor = "-"

                limite_max_valor = "-"

                parametro_config = next(

                    (
                        item
                        for item in parametros_cadastrados
                        if item["nome"] == parametro
                    ),

                    None
                )

                # =========================================
                # LIMITES
                # =========================================

                if parametro_config:

                    limite_min_valor = (

                        parametro_config["limite_min"]
                    )

                    limite_max_valor = (

                        parametro_config["limite_max"]
                    )

                # =========================================
                # VALIDATION ENGINE
                # =========================================

                resultado_validacao = validar_parametro(

                    valor,

                    limite_min_valor,

                    limite_max_valor
                )

                status = resultado_validacao["status"]

                criticidade = resultado_validacao["criticidade"]

                desvio = resultado_validacao["desvio"]

                cor = resultado_validacao["cor"]

                # =========================================
                # ALERTAS
                # =========================================

                if status != "Conforme":

                    total_alertas += 1

                # =========================================
                # RESULTADO ESTRUTURADO
                # =========================================

                resultados_processados[parametro] = {

                    "valor": valor,

                    "status": status,

                    "criticidade": criticidade,

                    "cor": cor,

                    "limite_min": limite_min_valor,

                    "limite_max": limite_max_valor,

                    "desvio": desvio
                }

            # =============================================
            # STATUS GERAL
            # =============================================

            status_geral = "Conforme"

            for resultado in resultados_processados.values():

                if resultado["status"] == "Preditivo":

                    status_geral = "Preditivo"

                if resultado["status"] == "Crítico":

                    status_geral = "Crítico"

            # =============================================
            # NOVA COLETA
            # =============================================

            nova_coleta = {

                "timestamp": datetime.now(),

                "ponto": ponto,

                "planta": planta,

                "setor": setor,

                "operador": st.session_state.user_name,

                "data_coleta": str(data_coleta),

                "hora_coleta": str(hora_coleta),

                "resultados": resultados_processados,

                "observacoes": observacoes,

                "status": status_geral
            }

            # =============================================
            # SALVA COLETA SESSION
            # =============================================

            st.session_state.coletas.append(
                nova_coleta
            )

            # =============================================
            # SALVA NO POSTGRESQL
            # =============================================

            conn = get_safe_connection()

            cursor = conn.cursor()

            sql = """

            INSERT INTO collections (

                data_coleta,
                hora_coleta,
                ponto,
                operador,
                status,
                resultados,
                planta,
                setor,
                observacoes

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s

            )

            """

            valores = (

                str(data_coleta),
                str(hora_coleta),
                ponto,
                st.session_state.user_name,
                status_geral,
                json.dumps(resultados_processados),
                planta,
                setor,
                observacoes

            )

            cursor.execute(sql, valores)

            conn.commit()

            cursor.close()

            # =============================================
            # AUDITORIA
            # =============================================

            registrar_auditoria(

                usuario=st.session_state.user_name,

                role=st.session_state.role,

                acao="REGISTROU COLETA",

                detalhes=f"{ponto} | Alertas: {total_alertas}"
            )

            # =============================================
            # FEEDBACK
            # =============================================

            if total_alertas > 0:

                st.warning(
                    f"⚠️ Coleta registrada com {total_alertas} alerta(s)."
                )

            else:

                st.success(
                    "✅ Coleta registrada com sucesso!"
                )

            st.toast(
                "Coleta adicionada ao sistema operacional."
            )

            st.rerun()

    st.divider()