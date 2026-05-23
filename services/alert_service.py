import streamlit as st


# =========================================================
# ORDENAR COLETAS
# =========================================================

def obter_coletas_ordenadas():

    if "coletas" not in st.session_state:

        return []

    return sorted(

        st.session_state.coletas,

        key=lambda x: (

            x["data_coleta"],

            x["hora_coleta"]
        )
    )


# =========================================================
# HISTÓRICO PARÂMETRO
# =========================================================

def obter_historico_parametro(

    parametro
):

    historico = []

    coletas = obter_coletas_ordenadas()

    for coleta in coletas:

        resultados = coleta["resultados"]

        if parametro in resultados:

            historico.append(

                resultados[parametro]
            )

    return historico


# =========================================================
# ALERTAS CONSECUTIVOS
# =========================================================

def verificar_alertas_consecutivos(

    parametro
):

    historico = obter_historico_parametro(

        parametro
    )

    if len(historico) < 2:

        return 0

    consecutivos = 0

    for item in reversed(historico):

        if item["status"] == "Alerta":

            consecutivos += 1

        else:

            break

    return consecutivos


# =========================================================
# TENDÊNCIA OPERACIONAL
# =========================================================

def verificar_tendencia(

    parametro,

    quantidade=3
):

    historico = obter_historico_parametro(

        parametro
    )

    if len(historico) < quantidade:

        return None

    valores = []

    for item in historico[-quantidade:]:

        try:

            valores.append(

                float(item["valor"])
            )

        except:

            return None

    crescente = (

        valores[0]

        <

        valores[1]

        <

        valores[2]
    )

    decrescente = (

        valores[0]

        >

        valores[1]

        >

        valores[2]
    )

    if crescente:

        return "crescente"

    if decrescente:

        return "decrescente"

    return None


# =========================================================
# ALERTA PREDITIVO
# =========================================================

def verificar_alerta_preditivo(

    parametro,

    margem=0.9
):

    historico = obter_historico_parametro(

        parametro
    )

    if not historico:

        return False

    ultimo = historico[-1]

    try:

        valor = float(

            ultimo["valor"]
        )

        limite_max = float(

            ultimo["limite_max"]
        )

        limite_min = float(

            ultimo["limite_min"]
        )

    except:

        return False

    proximidade_max = (

        valor >= limite_max * margem
    )

    proximidade_min = (

        valor <= limite_min * (1 + (1 - margem))
    )

    return proximidade_max or proximidade_min


# =========================================================
# PARÂMETRO CRÍTICO
# =========================================================

def verificar_parametro_critico(

    parametro
):

    if "parameters" not in st.session_state:

        return False

    for item in st.session_state.parameters:

        if item["nome"] == parametro:

            return item.get("critico", False)

    return False


# =========================================================
# CLASSIFICAÇÃO RISCO
# =========================================================

def classificar_risco(

    consecutivos,

    tendencia,

    critico
):

    if consecutivos >= 3:

        return "🔴 CRÍTICO"

    if consecutivos == 2:

        return "🟠 ALTO"

    if tendencia:

        return "🟡 MÉDIO"

    if critico:

        return "🟠 ALTO"

    return "🟢 NORMAL"


# =========================================================
# ANALISAR ALERTAS
# =========================================================

def analisar_alertas():

    alertas = []

    # =====================================================
    # SEM DADOS
    # =====================================================

    if "coletas" not in st.session_state:

        return [

            {

                "tipo": "ℹ️ ENGINE",

                "mensagem": "Nenhuma coleta disponível para análise."
            }
        ]

    if len(st.session_state.coletas) == 0:

        return [

            {

                "tipo": "ℹ️ ENGINE",

                "mensagem": "Nenhuma coleta registrada."
            }
        ]

    # =====================================================
    # MAPEAR PARÂMETROS
    # =====================================================

    parametros = set()

    for coleta in st.session_state.coletas:

        for parametro in coleta["resultados"].keys():

            parametros.add(parametro)

    # =====================================================
    # ANALISAR
    # =====================================================

    for parametro in parametros:

        consecutivos = verificar_alertas_consecutivos(

            parametro
        )

        tendencia = verificar_tendencia(

            parametro
        )

        preditivo = verificar_alerta_preditivo(

            parametro
        )

        critico = verificar_parametro_critico(

            parametro
        )

        risco = classificar_risco(

            consecutivos,

            tendencia,

            critico
        )

        # =================================================
        # ALERTA CRÍTICO
        # =================================================

        if consecutivos >= 3:

            alertas.append({

                "tipo": "🚨 ALERTA CRÍTICO",

                "parametro": parametro,

                "mensagem": f"{parametro} possui múltiplos desvios consecutivos.",

                "risco": risco
            })

        # =================================================
        # ALERTA ALTO
        # =================================================

        elif consecutivos == 2:

            alertas.append({

                "tipo": "⚠️ ALERTA ALTO",

                "parametro": parametro,

                "mensagem": f"{parametro} possui desvios consecutivos.",

                "risco": risco
            })

        # =================================================
        # TENDÊNCIA
        # =================================================

        if tendencia == "crescente":

            alertas.append({

                "tipo": "📈 TENDÊNCIA DE ALTA",

                "parametro": parametro,

                "mensagem": f"{parametro} apresenta crescimento contínuo.",

                "risco": risco
            })

        elif tendencia == "decrescente":

            alertas.append({

                "tipo": "📉 TENDÊNCIA DE QUEDA",

                "parametro": parametro,

                "mensagem": f"{parametro} apresenta queda contínua.",

                "risco": risco
            })

        # =================================================
        # ALERTA PREDITIVO
        # =================================================

        if preditivo:

            alertas.append({

                "tipo": "⚠️ ALERTA PREDITIVO",

                "parametro": parametro,

                "mensagem": f"{parametro} está próximo do limite operacional.",

                "risco": risco
            })

    # =====================================================
    # ENGINE NORMAL
    # =====================================================

    if not alertas:

        alertas.append({

            "tipo": "ℹ️ ENGINE",

            "parametro": "-",

            "mensagem": "Nenhum padrão crítico identificado até o momento.",

            "risco": "🟢 NORMAL"
        })

    return alertas
