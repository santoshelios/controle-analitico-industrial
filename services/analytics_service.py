import streamlit as st
import pandas as pd

from services.date_filter_service import (
    filtrar_coletas
)

# =========================================================
# STATUS CRÍTICOS
# =========================================================

STATUS_ALERTA = [

    "Preditivo",

    "Moderado",

    "Crítico"
]

# =========================================================
# COLETAS FILTRADAS
# =========================================================

def get_coletas_filtradas():

    if "coletas" not in st.session_state:

        return []

    return filtrar_coletas(
        st.session_state.coletas
    )

# =========================================================
# TOTAL COLETAS
# =========================================================

def total_coletas():

    return len(
        get_coletas_filtradas()
    )

# =========================================================
# TOTAL ALERTAS
# =========================================================

def total_alertas():

    total = 0

    for coleta in get_coletas_filtradas():

        for resultado in coleta["resultados"].values():

            if resultado["status"] in STATUS_ALERTA:

                total += 1

    return total

# =========================================================
# TOTAL CONFORMES
# =========================================================

def total_conformes():

    total = 0

    for coleta in get_coletas_filtradas():

        for resultado in coleta["resultados"].values():

            if resultado["status"] == "Conforme":

                total += 1

    return total

# =========================================================
# TAXA CONFORMIDADE
# =========================================================

def taxa_conformidade():

    conformes = total_conformes()

    alertas = total_alertas()

    total = conformes + alertas

    if total == 0:

        return 0

    return round(
        (conformes / total) * 100,
        1
    )

# =========================================================
# TOTAL PONTOS
# =========================================================

def total_pontos():

    if "collection_points" not in st.session_state:

        return 0

    return len(
        st.session_state.collection_points
    )

# =========================================================
# TOTAL PARÂMETROS
# =========================================================

def total_parametros():

    if "parameters" not in st.session_state:

        return 0

    return len(
        st.session_state.parameters
    )

# =========================================================
# ÚLTIMAS COLETAS
# =========================================================

def ultimas_coletas(limite=10):

    linhas = []

    coletas_recentes = list(
        reversed(
            get_coletas_filtradas()[-limite:]
        )
    )

    for coleta in coletas_recentes:

        for parametro, resultado in coleta["resultados"].items():

            linhas.append({

                "Data": coleta["data_coleta"],

                "Hora": coleta["hora_coleta"],

                "Ponto": coleta["ponto"],

                "Parâmetro": parametro,

                "Valor": resultado["valor"],

                "Status": resultado["status"],

                "Desvio": resultado["desvio"],

                "Operador": coleta["operador"]
            })

    return pd.DataFrame(linhas)

# =========================================================
# SCORE OPERACIONAL
# =========================================================

def score_operacional():

    coletas = get_coletas_filtradas()

    if len(coletas) == 0:

        return "Sem Dados"

    score = 100

    for coleta in coletas:

        for resultado in coleta["resultados"].values():

            status = resultado["status"]

            if status == "Preditivo":

                score -= 5

            elif status == "Moderado":

                score -= 12

            elif status == "Crítico":

                score -= 25

    score = max(score, 0)

    if score >= 90:

        return "Excelente"

    elif score >= 75:

        return "Bom"

    elif score >= 50:

        return "Atenção"

    else:

        return "Crítico"

# =========================================================
# RANKING PARÂMETROS CRÍTICOS
# =========================================================

def ranking_parametros_criticos():

    ranking = {}

    for coleta in get_coletas_filtradas():

        for parametro, resultado in coleta["resultados"].items():

            if resultado["status"] in STATUS_ALERTA:

                if parametro not in ranking:

                    ranking[parametro] = 0

                ranking[parametro] += 1

    return sorted(
        ranking.items(),
        key=lambda x: x[1],
        reverse=True
    )

# =========================================================
# RANKING PONTOS CRÍTICOS
# =========================================================

def ranking_pontos_criticos():

    ranking = {}

    for coleta in get_coletas_filtradas():

        ponto = coleta["ponto"]

        total = 0

        for resultado in coleta["resultados"].values():

            if resultado["status"] in STATUS_ALERTA:

                total += 1

        if total > 0:

            if ponto not in ranking:

                ranking[ponto] = 0

            ranking[ponto] += total

    return sorted(
        ranking.items(),
        key=lambda x: x[1],
        reverse=True
    )

# =========================================================
# TENDÊNCIA ALERTAS
# =========================================================

def tendencia_alertas():

    tendencia = {}

    for coleta in get_coletas_filtradas():

        data = coleta["data_coleta"]

        total = 0

        for resultado in coleta["resultados"].values():

            if resultado["status"] in STATUS_ALERTA:

                total += 1

        if data not in tendencia:

            tendencia[data] = 0

        tendencia[data] += total

    return sorted(
        tendencia.items(),
        key=lambda x: x[0]
    )