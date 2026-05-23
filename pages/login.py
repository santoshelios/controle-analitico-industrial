import streamlit as st
from services.audit_service import registrar_auditoria


# =========================================================
# USUÁRIOS MOCK
# =========================================================

usuarios_mock = [

    {
        "usuario": "master",
        "senha": "123",
        "nome": "Administrador Master",
        "role": "master"
    },

    {
        "usuario": "supervisor",
        "senha": "123",
        "nome": "Supervisor Industrial",
        "role": "master"
    },

    {
        "usuario": "operador",
        "senha": "123",
        "nome": "Operador Industrial",
        "role": "user"
    }
]




# =========================================================
# LOGIN
# =========================================================

def show_login():

    st.markdown("""
    <div class="status">
    🔒 Segurança Corporativa
    </div>

    <div class="status">
    ⚡ Ambiente Enterprise
    </div>

    <div class="status">
    🏭 Controle Industrial
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
    Controle Analítico Industrial
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-subtitle">
    Plataforma corporativa para monitoramento,
    rastreabilidade e inteligência operacional
    aplicada à engenharia industrial.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:

        usuario_input = st.text_input(
            "Usuário",
            placeholder="Digite seu usuário"
        )

        senha_input = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha"
        )

        if st.button("ENTRAR NO SISTEMA"):

            usuario_encontrado = next(

                (
                    item
                    for item in usuarios_mock

                    if (
                        item["usuario"] == usuario_input
                        and
                        item["senha"] == senha_input
                    )
                ),

                None
            )

            if usuario_encontrado:

                st.session_state.logged_in = True

                st.session_state.user_name = (

                    usuario_encontrado["nome"]
                )

                st.session_state.role = (

                    usuario_encontrado["role"]
                )

                st.session_state.user_login = (

                    usuario_encontrado["usuario"]
                )

                # =====================================
                # AUDITORIA LOGIN
                # =====================================

                registrar_auditoria(

                    usuario=usuario_encontrado["nome"],

                    role=usuario_encontrado["role"],

                    acao="LOGIN",

                    detalhes="Usuário acessou o sistema"
                )

                st.rerun()

            else:

                st.error(
                    "Usuário ou senha inválidos."
                )

    with st.sidebar:

        st.markdown("""
        # 🏭 Industrial Control

        Secure Enterprise Access
        """)

        st.divider()

        st.markdown("""
### Plataforma Enterprise

- Controle Industrial
- Engenharia Analítica
- Energia & Biomassa
- Auditoria Técnica
- Rastreabilidade
""")