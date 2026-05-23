import streamlit as st
import pandas as pd

from components.premium_table import (
    render_premium_table
)


# =========================================================
# USER MANAGEMENT
# =========================================================

def show_user_management():

    st.title("👥 Gestão de Usuários")

    st.markdown("""
    Gestão corporativa de acessos e permissões da plataforma.
    """)

    st.divider()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "users_registry" not in st.session_state:

        st.session_state.users_registry = []

    if "plants" not in st.session_state:

        st.session_state.plants = []

    role = st.session_state.role

    # =====================================================
    # SOMENTE MASTER
    # =====================================================

    if role != "master":

        st.warning(
            "🔒 Apenas administradores master possuem acesso."
        )

        return

    # =====================================================
    # FORMULÁRIO
    # =====================================================

    with st.form("form_users"):

        st.subheader("👤 Cadastro de Usuário")

        col1, col2 = st.columns(2)

        # =================================================
        # COLUNA 1
        # =================================================

        with col1:

            nome = st.text_input(
                "Nome Completo"
            )

            usuario = st.text_input(
                "Usuário"
            )

            senha = st.text_input(

                "Senha Temporária",

                type="password"
            )

        # =================================================
        # COLUNA 2
        # =================================================

        with col2:

            role_user = st.selectbox(

                "Perfil de Acesso",

                [
                    "master",
                    "operador"
                ]
            )

            status = st.selectbox(

                "Status",

                [
                    "Ativo",
                    "Inativo"
                ]
            )

            plantas_options = [

                 "🌐 Todas as Plantas"
            ] + [     

                item["Planta"]

                for item in st.session_state.plants
            ]

            plantas_permitidas = st.multiselect(

                "Plantas Permitidas",

                plantas_options
            )

        salvar = st.form_submit_button(
            "Salvar Usuário"
        )

        # =================================================
        # SALVAR
        # =================================================

        if salvar:

            if not nome or not usuario or not senha:

                st.warning(
                    "Preencha todos os campos obrigatórios."
                )

            else:

                st.session_state.users_registry.append({

                    "Nome": nome,

                    "Usuário": usuario,

                    "Senha": senha,

                    "Perfil": role_user,

                    "Status": status,

                    "Plantas": plantas_permitidas
                })

                st.success(
                    "Usuário cadastrado com sucesso."
                )

                st.rerun()

    st.divider()

    # =====================================================
    # TABELA
    # =====================================================

    st.subheader("📋 Usuários Cadastrados")

    if st.session_state.users_registry:

        tabela = []

        for item in st.session_state.users_registry:

            linha = {

                "Nome": item["Nome"],

                "Usuário": item["Usuário"],

                "Perfil": item["Perfil"],

                "Status": item["Status"],

                "Plantas": ", ".join(
                    item["Plantas"]
                )
            }

            tabela.append(linha)

        df = pd.DataFrame(tabela)

        render_premium_table(
            df.reset_index(drop=True)
        )

    else:

        st.info(
            "Nenhum usuário cadastrado."
        )