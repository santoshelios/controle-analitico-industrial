import streamlit as st


# =========================================================
# VALIDAR PONTO
# =========================================================

def validar_ponto(

    nome,
    parametros
):

    if nome.strip() == "":

        return False, "Nome do ponto obrigatório."

    if len(parametros) == 0:

        return False, "Selecione ao menos 1 parâmetro."

    return True, ""


# =========================================================
# CRIAR PONTO
# =========================================================

def criar_ponto(

    nome,
    planta,
    setor,
    tipo,
    status,
    criticidade,
    parametros,
    observacoes
):

    novo_ponto = {

        "nome": nome,

        "planta": planta,

        "setor": setor,

        "tipo": tipo,

        "status": status,

        "criticidade": criticidade,

        "parametros": parametros,

        "observacoes": observacoes
    }

    st.session_state.collection_points.append(
        novo_ponto
    )


# =========================================================
# EXCLUIR PONTO
# =========================================================

def excluir_ponto(

    nome_ponto
):

    st.session_state.collection_points = [

        item

        for item
        in st.session_state.collection_points

        if item["nome"] != nome_ponto
    ]