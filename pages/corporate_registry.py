import streamlit as st
import pandas as pd

from components.premium_table import (
    render_premium_table
)

from db_connection import get_safe_connection

# =========================================================
# CORPORATE REGISTRY
# =========================================================

def show_corporate_registry():

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "units" not in st.session_state:

        st.session_state.units = []

    if "plants" not in st.session_state:

        st.session_state.plants = []

    if "sectors" not in st.session_state:

        st.session_state.sectors = []

    if "categories" not in st.session_state:

        st.session_state.categories = []

    if "operational_types" not in st.session_state:
        st.session_state.operational_types = []

    # =====================================================
    # HEADER
    # =====================================================

    st.title("⚙️ Cadastros Corporativos")

    st.markdown("""
    Estrutura organizacional corporativa da plataforma.
    """)

    st.divider()

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4,tab5 = st.tabs([

        "🏭 Unidades",

        "🏢 Plantas",

        "🧩 Setores",

        "🧪 Categorias",

        "🏷️ Tipos Operacionais"
    ])

    # =====================================================
    # UNIDADES
    # =====================================================

    with tab1:

        st.subheader("🏭 Cadastro de Unidades")

        with st.form("form_units"):

            col1, col2 = st.columns(2)

            with col1:

                unit_name = st.text_input(
                    "Nome da Unidade"
                )

            with col2:

                unit_status = st.selectbox(

                    "Status",

                    [

                        "Ativo",

                        "Inativo"
                    ]
                )

            unit_desc = st.text_area(
                "Descrição"
            )

            submit_unit = st.form_submit_button(
                "Salvar Unidade"
            )
            if submit_unit:

                if unit_name:

                    # =====================================
                    # SESSION STATE
                    # =====================================

                    st.session_state.units.append({

                        "Nome": unit_name,

                        "Status": unit_status,

                        "Descrição": unit_desc
                    })

                    # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    sql = """

                    INSERT INTO units (

                        nome,
                        status,
                        descricao

                    )

                    VALUES (

                        %s,
                        %s,
                        %s

                    )

                    """

                    valores = (

                        unit_name,
                        unit_status,
                        unit_desc

                    )

                    cursor.execute(sql, valores)

                    conn.commit()

                    cursor.close()

                    st.success(
                        "Unidade cadastrada com sucesso."
                    )

                else:

                    st.warning(
                        "Informe o nome da unidade."
                    )

        st.divider()

        if len(st.session_state.units) > 0:

            df_units = pd.DataFrame(
                st.session_state.units
            )

            render_premium_table(df_units)

    # =====================================================
    # PLANTAS
    # =====================================================

    with tab2:

        st.subheader("🏢 Cadastro de Plantas")

        with st.form("form_plants"):

            col1, col2 = st.columns(2)

            with col1:

                plant_name = st.text_input(
                    "Nome da Planta"
                )

            with col2:

                units_options = [

                    item["Nome"]

                    for item in st.session_state.units
                ]

                if len(units_options) == 0:

                    units_options = [
                        "Nenhuma unidade cadastrada"
                    ]

                plant_unit = st.selectbox(

                    "Unidade",

                    units_options
                )

            plant_desc = st.text_input(
                "Descrição Operacional"
            )

            submit_plant = st.form_submit_button(
                "Salvar Planta"
            )

            if submit_plant:

                if plant_name:

                    # =====================================
                    # SESSION STATE
                    # =====================================

                    st.session_state.plants.append({

                        "Planta": plant_name,

                        "Unidade": plant_unit,

                        "Descrição": plant_desc
                    })

                    # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    sql = """

                    INSERT INTO plants (

                        nome,
                        cidade,
                        estado,
                        status,
                        observacoes

                    )

                    VALUES (

                        %s,
                        %s,
                        %s,
                        %s,
                        %s

                    )

                    """

                    valores = (

                        plant_name,
                        "-",
                        "-",
                        "Ativo",
                        plant_desc

                    )

                    cursor.execute(sql, valores)

                    conn.commit()

                    cursor.close()

                    st.success(
                        "Planta cadastrada com sucesso."
                    )

                else:

                    st.warning(
                        "Informe o nome da planta."
                    )

            else:

                    st.warning(
                        "Informe o nome da planta."
                    )

        st.divider()

        if len(st.session_state.plants) > 0:

            df_plants = pd.DataFrame(
                st.session_state.plants
            )

            render_premium_table(df_plants)

    # =====================================================
    # SETORES
    # =====================================================

    with tab3:

        st.subheader("🧩 Cadastro de Setores")

        with st.form("form_sectors"):

            col1, col2 = st.columns(2)

            with col1:

                sector_name = st.text_input(
                    "Nome do Setor"
                )

            with col2:

                plants_options = [

                    item["Planta"]

                    for item in st.session_state.plants
                ]

                if len(plants_options) == 0:

                    plants_options = [
                        "Nenhuma planta cadastrada"
                    ]

                sector_plant = st.selectbox(

                    "Planta",

                    plants_options
                )

            sector_desc = st.text_area(
                "Descrição Técnica"
            )

            submit_sector = st.form_submit_button(
                "Salvar Setor"
            )

            if submit_sector:

                if sector_name:

                    # =====================================
                    # SESSION STATE
                    # =====================================

                    st.session_state.sectors.append({

                        "Setor": sector_name,

                        "Planta": sector_plant,

                        "Descrição": sector_desc
                    })

                    # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    sql = """

                    INSERT INTO sectors (

                        nome,
                        planta,
                        descricao

                    )

                    VALUES (

                        %s,
                        %s,
                        %s

                    )

                    """

                    valores = (

                        sector_name,
                        sector_plant,
                        sector_desc

                    )

                    cursor.execute(sql, valores)

                    conn.commit()

                    cursor.close()

                    st.success(
                        "Setor cadastrado com sucesso."
                    )

                else:

                    st.warning(
                        "Informe o nome do setor."
                    )

        st.divider()

        if len(st.session_state.sectors) > 0:

            df_sectors = pd.DataFrame(
                st.session_state.sectors
            )

            render_premium_table(df_sectors)

    # =====================================================
    # CATEGORIAS
    # =====================================================

    with tab4:

        st.subheader("🧪 Cadastro de Categorias")

        with st.form("form_categories"):

            category_name = st.text_input(
                "Nome da Categoria"
            )

            category_desc = st.text_area(
                "Descrição Técnica"
            )

            submit_category = st.form_submit_button(
                "Salvar Categoria"
            )

            if submit_category:

                if category_name:

                    # =====================================
                    # SESSION STATE
                    # =====================================

                    st.session_state.categories.append({

                        "Categoria": category_name,

                        "Descrição": category_desc
                    })

                    # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    sql = """

                    INSERT INTO categories (

                        nome,
                        descricao

                    )

                    VALUES (

                        %s,
                        %s

                    )

                    """

                    valores = (

                        category_name,
                        category_desc

                    )

                    cursor.execute(sql, valores)

                    conn.commit()

                    cursor.close()

                    st.success(
                        "Categoria cadastrada com sucesso."
                    )

                else:

                    st.warning(
                        "Informe o nome da categoria."
                    )

        st.divider()

        if len(st.session_state.categories) > 0:

            df_categories = pd.DataFrame(
                st.session_state.categories
            )

            render_premium_table(df_categories)

    # =====================================================
    # TIPOS OPERACIONAIS
    # =====================================================

    with tab5:

        st.subheader("🏷️ Tipos Operacionais")

        with st.form("form_operational_types"):

            operational_name = st.text_input(
                "Nome do Tipo Operacional"
            )

            operational_desc = st.text_area(
                "Descrição Operacional"
            )

            submit_operational = st.form_submit_button(
                "Salvar Tipo"
            )

            if submit_operational:

                if operational_name:

                    # =====================================
                    # SESSION STATE
                    # =====================================

                    st.session_state.operational_types.append({

                        "Tipo": operational_name,

                        "Descrição": operational_desc
                    })

                    # =====================================
                    # POSTGRESQL
                    # =====================================

                    conn = get_safe_connection()

                    cursor = conn.cursor()

                    sql = """

                    INSERT INTO operational_types (

                        nome,
                        descricao

                    )

                    VALUES (

                        %s,
                        %s

                    )

                    """

                    valores = (

                        operational_name,
                        operational_desc

                    )

                    cursor.execute(sql, valores)

                    conn.commit()

                    cursor.close()

                    st.success(
                        "Tipo operacional cadastrado com sucesso."
                    )

                else:

                    st.warning(
                        "Informe o nome do tipo operacional."
                    )

        st.divider()

        if st.session_state.operational_types:

            df_operational = pd.DataFrame(
                st.session_state.operational_types
            )

            render_premium_table(df_operational)