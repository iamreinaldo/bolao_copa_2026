import streamlit as st
from services.auth import login, logout
from services.footer import mostrar_rodape


st.set_page_config(
    page_title="Bolão Copa do Mundo",
    page_icon="⚽",
    layout="wide"
)

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "nome" not in st.session_state:
    st.session_state.nome = None

if not st.session_state.logado:
    st.title("⚽ Bolão da Copa")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if login(usuario, senha):
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

else:
    st.title("⚽ Bolão da Copa")

    st.success(
    f"Bem-vindo, {st.session_state.nome}!"
    )

    st.write("Use o menu lateral para acessar as páginas do bolão.")

    if st.session_state.usuario == "admin":
        st.info("Você está logado como administrador.")

    if st.button("Sair"):
        logout()
        st.rerun()


# Footer
mostrar_rodape()