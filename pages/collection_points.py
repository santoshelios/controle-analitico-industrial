import streamlit as st
import pandas as pd

from services.audit_service import registrar_auditoria

from services.collection_point_service import (

    validar_ponto,

    criar_ponto,

    excluir_ponto
)

from components.premium_table import (
    render_premium_table
)

import json

from db_connection import get_safe_connection

# =========================================================
# COLLECTION POINTS PAGE
# =========================================================

def show_collection_points():

    st.title("📍 Pontos de Coleta")

    st.markdown("""
    Cadastro operacional dos pontos de coleta
    monitorados pelo sistema analítico industrial.
    """)

    st.divider()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "collection_points" not in st.session_state:

        st.session_state.collection_points = []

    if "parameters" not in st.session_state:

        st.session_state.parameters = []

    role = st.session_state.role

    parametros_disponiveis = [

        item["nome"]

        for item in st.session_state.parameters
    ]

    # =====================================================
    # LOAD POSTGRESQL
    # =====================================================

    try:

        conn = get_safe_connection()

        cursor = conn.cursor()

        # =================================================
        # PONTOS DE COLETA
        # =================================================

        cursor.execute("""

            SELECT

                nome,

                planta,

                setor,

                tipo,

                status,

                criticidade,

                parametros

            FROM collection_points

            ORDER BY nome

        """)

        rows = cursor.fetchall()

        st.session_state.collection_points = []

        for row in rows:

            st.session_state.collection_points.append({

                "nome": row[0],

                "planta": row[1],

                "setor": row[2],

                "tipo": row[3],

                "status": row[4] if row[4] else "Ativo",

                "criticidade": row[5] if row[5] else "Média",

                "parametros": row[6] if row[6] else []
            })

        # =================================================
        # PLANTAS
        # =================================================

        cursor.execute("""

            SELECT nome

            FROM plants

            
            ORDER BY nome

        """)

        plantas_db = cursor.fetchall()

        plantas_options = [

            row[0]

            for row in plantas_db
        ]

        if not plantas_options:

            plantas_options = [
                "Nenhuma planta cadastrada"
            ]

        # =================================================
        # SETORES
        # =================================================

        cursor.execute("""

            SELECT nome

            FROM sectors

            

            ORDER BY nome

        """)

        setores_db = cursor.fetchall()

        setores_options = [

            row[0]

            for row in setores_db
        ]

        if not setores_options:

            setores_options = [
                "Nenhum setor cadastrado"
            ]

        # =================================================
        # TIPOS OPERACIONAIS
        # =================================================

        cursor.execute("""

            SELECT nome

            FROM operational_types

            

            ORDER BY nome

        """)

        tipos_db = cursor.fetchall()

        tipos_options = [

            row[0]

            for row in tipos_db
        ]

        if not tipos_options:

            tipos_options = [
                "Nenhum tipo operacional cadastrado"
            ]

        cursor.close()

    except Exception as e:

        st.error(f"Erro PostgreSQL: {e}")

        plantas_options = [
            "Nenhuma planta cadastrada"
        ]

        setores_options = [
            "Nenhum setor cadastrado"
        ]

        tipos_options = [
            "Nenhum tipo operacional cadastrado"
        ]

    # =====================================================
    # SOMENTE MASTER
    # =====================================================

    if role == "master":

        with st.form("form_collection_points"):

            st.subheader("🏭 Informações do Ponto")

            col1, col2 = st.columns(2)

            # =================================================
            # COLUNA 1
            # =================================================

            with col1:

                nome = st.text_input(
                    "Nome do Ponto"
                )

                planta = st.selectbox(

                    "Planta Industrial",

                    plantas_options
                )

                setor = st.selectbox(

                    "Setor",

                    setores_options
                )

            # =================================================
            # COLUNA 2
            # =================================================

            with col2:

                tipo = st.selectbox(

                    "Tipo do Ponto",

                    tipos_options
                )

                status = st.selectbox(

                    "Status",

                    [
                        "Ativo",
                        "Inativo"
                    ]
                )

                criticidade = st.selectbox(

                    "Criticidade",

                    [
                        "Baixa",
                        "Média",
                        "Alta"
                    ]
                )

            st.divider()

            st.subheader("🧪 Parâmetros Vinculados")

            parametros_vinculados = st.multiselect(

                "Selecione os parâmetros",

                parametros_disponiveis
            )

            observacoes = st.text_area(

                "Observações Operacionais",

                height=120
            )

            salvar = st.form_submit_button(
                "Salvar Ponto"
            )

            # =================================================
            # SALVAR
            # =================================================

            if salvar:

                validacao, mensagem = validar_ponto(

                    nome=nome,

                    parametros=parametros_vinculados
                )

                # =============================================
                # VALIDAÇÃO
                # =============================================

                if not validacao:

                    st.error(mensagem)

                else:

                    criar_ponto(

                        nome=nome,

                        planta=planta,

                        setor=setor,

                        tipo=tipo,

                        status=status,

                        criticidade=criticidade,

                        parametros=parametros_vinculados,

                        observacoes=observacoes
                    )

                    # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    sql = """

                    INSERT INTO collection_points (

                        nome,
                        setor,
                        planta,
                        tipo,
                        status,
                        criticidade,
                        observacoes,
                        parametros

                    )

                    VALUES (

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

                        nome,
                        setor,
                        planta,
                        tipo,
                        status,
                        criticidade,
                        observacoes,
                        json.dumps(parametros_vinculados)

                    )

                    cursor.execute(sql, valores)

                    conn.commit()

                    cursor.close()

                    # =========================================
                    # AUDITORIA
                    # =========================================

                    registrar_auditoria(

                        usuario=st.session_state.user_name,

                        role=role,

                        acao="CRIOU PONTO",

                        detalhes=nome
                    )

                    st.success(
                        "✅ Ponto cadastrado com sucesso!"
                    )

                    st.toast(
                        "Ponto operacional registrado."
                    )

                    st.rerun()

    else:

        st.info(
            "🔒 Apenas administradores master podem alterar pontos de coleta."
        )

    st.divider()

    # =====================================================
    # TABELA
    # =====================================================

    st.subheader("📋 Pontos Cadastrados")

    if st.session_state.collection_points:

        tabela = []

        for item in st.session_state.collection_points:

            linha = {

                "Nome": item["nome"],

                "Planta": item["planta"],

                "Setor": item["setor"],

                "Tipo": item["tipo"],

                "Status": item["status"],

                "Criticidade": item["criticidade"],

                "Parâmetros": ", ".join(
                    item["parametros"]
                )
            }

            tabela.append(linha)

        df = pd.DataFrame(tabela)

        render_premium_table(
            df.reset_index(drop=True)
        )

        # =================================================
        # ADMINISTRAÇÃO
        # =================================================

        if role == "master":

            st.divider()

            st.subheader("⚙️ Administração")

            nomes_pontos = [

                item["nome"]

                for item in st.session_state.collection_points
            ]

            ponto_admin = st.selectbox(

                "Selecionar Ponto",

                nomes_pontos
            )

            ponto_selecionado = next(

                (
                    item
                    for item in st.session_state.collection_points
                    if item["nome"] == ponto_admin
                ),

                None
            )

            if ponto_selecionado:

                with st.container(border=True):

                    st.markdown(

                        f"""
### 📍 {ponto_selecionado['nome']}

**Planta:** {ponto_selecionado['planta']}

**Setor:** {ponto_selecionado['setor']}

**Criticidade:** {ponto_selecionado['criticidade']}
"""
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "✏️ Editar Ponto"
                        ):

                            st.warning(
                                "🛠️ Edição completa será implementada na próxima sprint."
                            )

                    with col2:

                        if st.button(
                            "🗑️ Excluir Ponto"
                        ):

                            excluir_ponto(
                                ponto_admin
                            )

                            registrar_auditoria(

                                usuario=st.session_state.user_name,

                                role=role,

                                acao="EXCLUIU PONTO",

                                detalhes=ponto_admin
                            )

                            st.success(
                                "Ponto removido."
                            )

                            st.rerun()

    else:

        st.info(
            "Nenhum ponto cadastrado."
        )