import streamlit as st
from services.sqlite import buscar_usuario


def login(usuario, senha):
    user = buscar_usuario(usuario, senha)

    if not user:
        return False

    if str(user["senha"]) != senha:
        return False

    st.session_state.logado = True
    st.session_state.usuario_id = user["id"]
    st.session_state.usuario = user["usuario"]
    st.session_state.nome = user["nome"]
    st.session_state.modo_mobile = bool(
        user.get("modo_mobile", 0)
    )

    return True


def logout():
    st.session_state.logado = False
    st.session_state.usuario_id = None
    st.session_state.usuario = None
    st.session_state.nome = None
    st.session_state.modo_mobile = False