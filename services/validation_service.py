# =========================================================
# VALIDAÇÃO ANALÍTICA INTELIGENTE
# =========================================================

def validar_resultado(

    valor,
    limite_min,
    limite_max
):

    status = "Conforme"

    desvio = "-"

    try:

        valor_float = float(valor)

        # =====================================================
        # LIMITE MÍNIMO
        # =====================================================

        if limite_min != "":

            limite_min_float = float(limite_min)

            if valor_float < limite_min_float:

                diferenca = abs(

                    valor_float
                    - limite_min_float
                )

                percentual = (

                    diferenca
                    / limite_min_float
                ) * 100

                if percentual <= 10:

                    status = "Preditivo"

                elif percentual <= 30:

                    status = "Moderado"

                else:

                    status = "Crítico"

                desvio = f"-{diferenca:.2f}"

        # =====================================================
        # LIMITE MÁXIMO
        # =====================================================

        if limite_max != "":

            limite_max_float = float(limite_max)

            if valor_float > limite_max_float:

                diferenca = (

                    valor_float
                    - limite_max_float
                )

                percentual = (

                    diferenca
                    / limite_max_float
                ) * 100

                if percentual <= 10:

                    status = "Preditivo"

                elif percentual <= 30:

                    status = "Moderado"

                else:

                    status = "Crítico"

                desvio = f"+{diferenca:.2f}"

    except:

        status = "Erro"

        desvio = "-"

    return {

        "status": status,

        "desvio": desvio
    }