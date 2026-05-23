import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

from db_connection import get_safe_connection


# =========================================================
# TREND ANALYSIS
# =========================================================

def show_trend_analysis():

    st.title("📈 Trend Analysis")

    st.markdown("""
    Análise temporal multivariável industrial.
    """)

    st.divider()

    # =====================================================
    # LOAD POSTGRESQL
    # =====================================================

    conn = get_safe_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT

            data_coleta,
            hora_coleta,
            ponto,
            operador,
            status,
            resultados,
            planta,
            setor

        FROM collections

        ORDER BY data_coleta ASC

        """

    )

    rows = cursor.fetchall()

    cursor.close()

    # =====================================================
    # DATAFRAME
    # =====================================================

    dados = []

    for row in rows:

        data = str(row[0])

        hora = str(row[1])

        ponto = row[2]

        operador = row[3]

        status = row[4]

        resultados = row[5]

        planta = row[6]

        setor = row[7]

        if resultados:

            for parametro, info in resultados.items():

                try:

                    valor = float(info["valor"])

                except:

                    valor = None

                dados.append({

                    "Data": data,

                    "Hora": hora,

                    "Ponto": ponto,

                    "Operador": operador,

                    "Status": status,

                    "Planta": planta,

                    "Setor": setor,

                    "Parâmetro": parametro,

                    "Valor": valor
                })

    df = pd.DataFrame(dados)

    # =====================================================
    # SEM DADOS
    # =====================================================

    if df.empty:

        st.warning(
            "Nenhuma coleta disponível."
        )

        return

    # =====================================================
    # FILTROS
    # =====================================================

    st.subheader("🎛️ Filtros Analíticos")

    col1, col2, col3 = st.columns(3)

    with col1:

        plantas = ["Todas"] + sorted(
            df["Planta"].dropna().unique().tolist()
        )

        filtro_planta = st.selectbox(

            "Planta",

            plantas
        )

    with col2:

        setores = ["Todos"] + sorted(
            df["Setor"].dropna().unique().tolist()
        )

        filtro_setor = st.selectbox(

            "Setor",

            setores
        )

    with col3:

        pontos = ["Todos"] + sorted(
            df["Ponto"].dropna().unique().tolist()
        )

        filtro_ponto = st.selectbox(

            "Ponto",

            pontos
        )

    # =====================================================
    # MULTI VARIÁVEL
    # =====================================================

    parametros = sorted(
        df["Parâmetro"].dropna().unique().tolist()
    )

    parametros_selecionados = st.multiselect(

        "Variáveis Analíticas",

        parametros,

        default=parametros[:1]
    )

    # =====================================================
    # FILTRAGEM
    # =====================================================

    if filtro_planta != "Todas":

        df = df[
            df["Planta"] == filtro_planta
        ]

    if filtro_setor != "Todos":

        df = df[
            df["Setor"] == filtro_setor
        ]

    if filtro_ponto != "Todos":

        df = df[
            df["Ponto"] == filtro_ponto
        ]

    if parametros_selecionados:

        df = df[
            df["Parâmetro"].isin(
                parametros_selecionados
            )
        ]

    # =====================================================
    # TIMESTAMP
    # =====================================================

    df["Timestamp"] = pd.to_datetime(

        df["Data"] + " " + df["Hora"]

    )

    df = df.sort_values("Timestamp")

       # =====================================================
    # FILTRO DE PERÍODO ANALÍTICO
    # =====================================================

    periodo = st.session_state.get(

        "periodo_analitico",

        "Hoje"
    )

    agora = pd.Timestamp.now()

    if periodo == "Hoje":

        inicio = agora.normalize()

        df = df[
            df["Timestamp"] >= inicio
        ]

    elif periodo == "7 Dias":

        inicio = agora - pd.Timedelta(days=7)

        df = df[
            df["Timestamp"] >= inicio
        ]

    elif periodo == "30 Dias":

        inicio = agora - pd.Timedelta(days=30)

        df = df[
            df["Timestamp"] >= inicio
        ]

      # =====================================================
    # CHART
    # =====================================================

    st.subheader("📊 Tendência Temporal")

    fig = go.Figure()

    cores = [

        "#3B82F6",
        "#22C55E",
        "#F59E0B",
        "#EF4444",
        "#8B5CF6",
        "#06B6D4"
    ]

    # =====================================================
    # MULTI AXIS
    # =====================================================

    multiplas_variaveis = len(parametros_selecionados) > 1

    for idx, parametro in enumerate(parametros_selecionados):

        df_param = df[
            df["Parâmetro"] == parametro
        ]

        eixo_y = "y"

        if multiplas_variaveis and idx > 0:

            eixo_y = f"y{idx+1}"

        fig.add_trace(

            go.Scatter(

                x=df_param["Timestamp"],

                y=df_param["Valor"],

                mode="lines+markers+text",

                text=df_param["Valor"],

                textposition="top center",

                line_shape="spline",

                name=parametro,

                yaxis=eixo_y,

                hovertemplate=

                "<b>%{fullData.name}</b><br>" +

                "Valor: %{y}<br>" +

                "Timestamp: %{x}<extra></extra>",

                line=dict(

                    width=4,

                    smoothing=0.7,

                    color=cores[idx % len(cores)]
                ),

                marker=dict(

                    size=8
                )
            )
        )

       # =====================================================
    # LIMITES OPERACIONAIS
    # =====================================================

    if len(parametros_selecionados) == 1:

        parametro_unico = parametros_selecionados[0]

        limite_min = None
        limite_max = None

        for row in rows:

            resultados = row[5]

            if resultados and parametro_unico in resultados:

                try:

                    limite_min = float(

                        resultados[parametro_unico]["limite_min"]

                    )

                    limite_max = float(

                        resultados[parametro_unico]["limite_max"]

                    )

                    break

                except:

                    pass

        # ============================================
        # LIMITE INFERIOR
        # ============================================

        if limite_min is not None:

            fig.add_hline(

                y=limite_min,

                line_dash="dash",

                line_width=3,

                line_color="#FBBF24",

                annotation_text="Limite Inferior",

                annotation_position="bottom right"
            )

        # ============================================
        # LIMITE SUPERIOR
        # ============================================

        if limite_max is not None:

            fig.add_hline(

                y=limite_max,

                line_dash="dash",

                line_width=3,

                line_color="#FF4D6D",

                annotation_text="Limite Superior",

                annotation_position="top right"
            )

    # =====================================================
    # LAYOUT
    # =====================================================

    layout_config = dict(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(

            color="white",

            family="Inter"
        ),

        height=650,

        hovermode="x unified",

        margin=dict(

            l=40,
            r=40,
            t=40,
            b=40
        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="left",

            x=0.01,

            font=dict(

                size=14,

                color="rgba(255,255,255,0.92)"
            ),

            bgcolor="rgba(15,23,42,0.72)",

            bordercolor="rgba(255,255,255,0.08)",

            borderwidth=1
        ),

        xaxis=dict(

            showgrid=False,

            zeroline=False
        ),

        yaxis=dict(

            title=parametros_selecionados[0]

            if parametros_selecionados

            else "",

            showgrid=True,

            gridcolor="rgba(255,255,255,0.025)",

            gridwidth=0.4,

            zeroline=False,

            color=cores[0]
        )
    )

    # =====================================================
    # MÚLTIPLOS EIXOS
    # =====================================================

    if multiplas_variaveis:

        for idx, parametro in enumerate(

            parametros_selecionados[1:],

            start=2
        ):

            layout_config[f"yaxis{idx}"] = dict(

                title=parametro,

                overlaying="y",

                side="right",

                showgrid=False,

                zeroline=False,

                color=cores[(idx-1) % len(cores)],

                position=min(

                    0.98,

                    1 - ((idx-2) * 0.05)
                )
            )

    fig.update_layout(

        **layout_config
    )

    st.plotly_chart(

        fig,

        use_container_width=True,
        key="trend_analysis_chart",
        config={

            "displaylogo": False,

            "modeBarButtonsToRemove": [

                "zoomIn2d",
                "zoomOut2d",
                "lasso2d",
                "select2d",
                "autoScale2d",
                "toggleSpikelines"
            ]
        }
    )

    