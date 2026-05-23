import streamlit as st


# =========================================================
# VALIDAR LIMITES
# =========================================================

def validar_limites(

    limite_min,
    limite_max
):

    if limite_max <= limite_min:

        return False

    return True


# =========================================================
# CRIAR PARÂMETRO
# =========================================================

def criar_parametro(

    nome,
    unidade,
    categoria,
    setor,
    tipo,
    limite_min,
    limite_max,
    casas_decimais,
    status,
    descricao,
    critico
):

    novo_parametro = {

        "nome": nome,

        "unidade": unidade,

        "categoria": categoria,

        "setor": setor,

        "tipo": tipo,

        "limite_min": limite_min,

        "limite_max": limite_max,

        "casas_decimais": casas_decimais,

        "status": status,

        "descricao": descricao,

        "critico": critico
    }

    st.session_state.parameters.append(
        novo_parametro
    )


# =========================================================
# EXCLUIR PARÂMETRO
# =========================================================

def excluir_parametro(

    nome_parametro
):

    st.session_state.parameters = [

        item

        for item
        in st.session_state.parameters

        if item["nome"] != nome_parametro
    ]