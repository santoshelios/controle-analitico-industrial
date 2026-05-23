import streamlit as st
import pandas as pd

from services.audit_service import registrar_auditoria

from services.parameter_service import (

    validar_limites,

    criar_parametro,

    excluir_parametro
)

from components.premium_table import (
    render_premium_table
)

from db_connection import get_safe_connection

# =========================================================
# PARAMETERS PAGE
# =========================================================

def show_parameters():

    st.title("🧪 Cadastro de Parâmetros")

    st.markdown("""
    Cadastro operacional de parâmetros analíticos
    utilizados no monitoramento industrial.
    """)

    st.divider()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "parameters" not in st.session_state:

        st.session_state.parameters = []

    if "categories" not in st.session_state:

        st.session_state.categories = []

   
    if "sectors" not in st.session_state:

        st.session_state.sectors = []

    role = st.session_state.role

        # =====================================================
    # LOAD POSTGRESQL
    # =====================================================

    try:

        conn = get_safe_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                nome,

                unidade,

                limite_min,

                limite_max,

                categoria,

                tipo_operacional

            FROM parameters

        """)

        rows = cursor.fetchall()

        st.session_state.parameters = []

        for row in rows:

            st.session_state.parameters.append({

                "nome": row[0],

                "unidade": row[1],

                "limite_min": row[2],

                "limite_max": row[3],

                "categoria": row[4],

                "tipo": row[5],

                "critico": False,

                "status": "Ativo"
            })

        cursor.close()

        

    except Exception as e:

        st.error(f"Erro PostgreSQL: {e}")

    # =====================================================
    # CADASTRO
    # =====================================================

    if role == "master":

        with st.form("form_parameter"):

            st.subheader("📋 Informações do Parâmetro")

            col1, col2 = st.columns(2)

            # =================================================
            # COLUNA 1
            # =================================================

            with col1:

                nome = st.text_input(
                    "Nome do Parâmetro"
                )

                unidade = st.text_input(
                    "Unidade"
                )

                # =============================================
                # CATEGORIAS CORPORATIVAS
                # =============================================

                categorias_options = [

                    item["Categoria"]

                    for item in st.session_state.categories
                ]

                if len(categorias_options) == 0:

                    categorias_options = [
                        "Nenhuma categoria cadastrada"
                    ]

                categoria = st.selectbox(

                    "Categoria",

                    categorias_options
                )

# =============================================
# SETORES CORPORATIVOS
# =============================================

                setores_options = [

                    item["Setor"]

                    for item in st.session_state.sectors
                ]

                if len(setores_options) == 0:

                    setores_options = [
                        "Nenhum setor cadastrado"
                    ]

                setor = st.selectbox(

                    "Setor Operacional",

                    setores_options
                )
                # =============================================
                # LIMITES
                # =============================================

                col_min, col_max = st.columns(2)

                with col_min:

                    limite_min = st.number_input(

                        "Limite Mínimo",

                        value=0.0
                    )

                with col_max:

                    limite_max = st.number_input(

                        "Limite Máximo",

                        value=0.0
                    )

            # =================================================
            # COLUNA 2
            # =================================================

            with col2:

                tipo = st.selectbox(

                    "Tipo do Parâmetro",

                    [
                        "Numérico",
                        "Texto",
                        "Booleano"
                    ]
                )

                casas_decimais = st.number_input(

                    "Casas Decimais",

                    min_value=0,

                    max_value=10,

                    value=2
                )

                status = st.selectbox(

                    "Status",

                    [
                        "Ativo",
                        "Inativo"
                    ]
                )

                critico = st.checkbox(
                    "Parâmetro Crítico"
                )

            descricao = st.text_area(

                "Descrição Técnica",

                height=120
            )

            salvar = st.form_submit_button(
                "Salvar Parâmetro"
            )

            # =================================================
            # SALVAR
            # =================================================

            if salvar:

                # =============================================
                # VALIDAÇÃO
                # =============================================

                if not validar_limites(

                    limite_min,

                    limite_max
                ):

                    st.error(
                        "⛔ O limite máximo deve ser maior que o limite mínimo."
                    )

                else:

                    criar_parametro(

                        nome=nome,

                        unidade=unidade,

                        categoria=categoria,

                        setor=setor,

                        tipo=tipo,

                        limite_min=limite_min,

                        limite_max=limite_max,

                        casas_decimais=casas_decimais,

                        status=status,

                        descricao=descricao,

                        critico=critico,
                        
                        
                    )



                                        # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    cursor.execute(

                        """

                        INSERT INTO parameters (

                            nome,

                            unidade,

                            limite_min,

                            limite_max,

                            categoria,

                            tipo_operacional,

                            planta,

                            setor

                        )

                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

                        """,

                        (

                            nome,

                            unidade,

                            limite_min,

                            limite_max,

                            categoria,

                            tipo,

                            "Corporativo",

                            setor
                        )
                    )

                    conn.commit()

                    cursor.close()

                    


                    # =========================================
                    # AUDITORIA
                    # =========================================

                    registrar_auditoria(

                        usuario=st.session_state.user_name,

                        role=role,

                        acao="CRIOU PARÂMETRO",

                        detalhes=nome
                    )

                    st.success(
                        "✅ Parâmetro salvo com sucesso!"
                    )

                    st.toast(
                        "Parâmetro operacional registrado."
                    )

                    st.rerun()

    else:

        st.info(
            "🔒 Apenas administradores master podem alterar parâmetros."
        )

    st.divider()

    # =====================================================
    # TABELA
    # =====================================================

    st.subheader("📋 Parâmetros Cadastrados")

    if st.session_state.parameters:

        tabela = []

        for item in st.session_state.parameters:

            linha = {

                "Nome": item["nome"],

                "Categoria": item["categoria"],

                "Tipo": item["tipo"],

                "Unidade": item["unidade"],

                "Limite Min": item["limite_min"],

                "Limite Max": item["limite_max"],

                "Crítico": "Sim"
                if item["critico"]
                else "Não",

                "Status": item["status"]
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

            nomes_parametros = [

                item["nome"]

                for item in st.session_state.parameters
            ]

            parametro_admin = st.selectbox(

                "Selecionar Parâmetro",

                nomes_parametros
            )

            parametro_selecionado = next(

                (
                    item
                    for item in st.session_state.parameters
                    if item["nome"] == parametro_admin
                ),

                None
            )

            if parametro_selecionado:

                with st.container(border=True):

                    st.markdown(

                        f"""
### 🧪 {parametro_selecionado['nome']}

**Categoria:** {parametro_selecionado['categoria']}

**Tipo:** {parametro_selecionado['tipo']}

**Limites:** {parametro_selecionado['limite_min']} / {parametro_selecionado['limite_max']}
"""
                    )

                    col1, col2 = st.columns(2)

                    # =====================================
                    # EDITAR
                    # =====================================

                    with col1:

                        if st.button(
                            "✏️ Editar Parâmetro"
                        ):

                            st.warning(
                                "🛠️ Edição completa será implementada na próxima sprint."
                            )

                    # =====================================
                    # EXCLUIR
                    # =====================================

                    with col2:

                        if st.button(
                            "🗑️ Excluir Parâmetro"
                        ):

                            excluir_parametro(
                                parametro_admin
                            )

                            registrar_auditoria(

                                usuario=st.session_state.user_name,

                                role=role,

                                acao="EXCLUIU PARÂMETRO",

                                detalhes=parametro_admin
                            )

                            st.success(
                                "Parâmetro removido."
                            )

                            st.rerun()

    else:

        st.info(
            "Nenhum parâmetro cadastrado."
        )