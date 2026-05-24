import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from db_connection import get_safe_connection


# =========================================================
# TREND ANALYSIS
# =========================================================

def show_trend_analysis():

    st.title("📈 Trend Analysis")

    st.markdown(
        """
        Análise temporal multivariável industrial.
        """
    )

    st.divider()

    # =====================================================
    # LOAD POSTGRESQL
    # =====================================================

    conn = get_safe_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT

            c.data_coleta,
            c.hora_coleta,
            c.ponto,
            c.operador,

            p.nome AS parametro,

            cr.valor,

            CASE
                WHEN cr.conforme = TRUE
                THEN 'Conforme'
                ELSE 'Crítico'
            END AS status,

            c.planta,
            c.setor,

            p.limite_min,
            p.limite_max

        FROM collection_results cr

        INNER JOIN collections c
            ON c.id = cr.collection_id

        INNER JOIN parameters p
            ON p.id = cr.parameter_id

        ORDER BY
            c.data_coleta ASC,
            c.hora_coleta ASC

        """

    )

    rows = cursor.fetchall()

    cursor.close()

    # =====================================================
    # DATAFRAME
    # =====================================================

    dados = []

    for row in rows:

        dados.append({

            "Data": str(row[0]),

            "Hora": str(row[1]),

            "Ponto": row[2],

            "Operador": row[3],

            "Parâmetro": row[4],

            "Valor": float(row[5]),

            "Status": row[6],

            "Planta": row[7],

            "Setor": row[8],

            "Limite Min": row[9],

            "Limite Max": row[10]
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
    # VARIÁVEIS ANALÍTICAS
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

    df = df.sort_values(
        "Timestamp"
    )

    # =====================================================
    # FILTRO PERÍODO ANALÍTICO
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

    multiplas_variaveis = (
        len(parametros_selecionados) > 1
    )

    # =====================================================
    # PLOTS
    # =====================================================

    for idx, parametro in enumerate(
        parametros_selecionados
    ):

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

        df_limite = df[
            df["Parâmetro"] == parametro_unico
        ]

        limite_min = df_limite[
            "Limite Min"
        ].dropna()

        limite_max = df_limite[
            "Limite Max"
        ].dropna()

        if not limite_min.empty:

            fig.add_hline(

                y=float(limite_min.iloc[0]),

                line_dash="dash",

                line_width=2,

                line_color="#FBBF24",

                annotation_text="Limite Inferior",

                annotation_position="bottom right"
            )

        if not limite_max.empty:

            fig.add_hline(

                y=float(limite_max.iloc[0]),

                line_dash="dash",

                line_width=2,

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
    # MULTI Y AXIS
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

    # =====================================================
    # RENDER
    # =====================================================

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