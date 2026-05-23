# =========================================================
# VALIDATION ENGINE
# =========================================================

def validar_parametro(

    valor,

    limite_min,

    limite_max
):

    try:

        valor = float(valor)

        limite_min = float(limite_min)

        limite_max = float(limite_max)

    except:

        return {

            "status": "Erro",

            "criticidade": "Erro",

            "desvio": 0,

            "cor": "#6B7280"
        }

    # =====================================================
    # FAIXA OPERACIONAL
    # =====================================================

    faixa = limite_max - limite_min

    margem = faixa * 0.10

    # =====================================================
    # DENTRO DA FAIXA
    # =====================================================

    if limite_min <= valor <= limite_max:

        return {

            "status": "Conforme",

            "criticidade": "Baixa",

            "desvio": 0,

            "cor": "#22C55E"
        }

    # =====================================================
    # PREDITIVO
    # =====================================================

    if (

        limite_min - margem <= valor < limite_min

    ) or (

        limite_max < valor <= limite_max + margem
    ):

        if valor < limite_min:

            desvio = round(

                ((valor - limite_min) / limite_min) * 100,

                2
            )

        else:

            desvio = round(

                ((valor - limite_max) / limite_max) * 100,

                2
            )

        return {

            "status": "Preditivo",

            "criticidade": "Moderada",

            "desvio": desvio,

            "cor": "#F59E0B"
        }

    # =====================================================
    # CRÍTICO
    # =====================================================

    if valor < limite_min:

        desvio = round(

            ((valor - limite_min) / limite_min) * 100,

            2
        )

    else:

        desvio = round(

            ((valor - limite_max) / limite_max) * 100,

            2
        )

    return {

        "status": "Crítico",

        "criticidade": "Alta",

        "desvio": desvio,

        "cor": "#EF4444"
    }