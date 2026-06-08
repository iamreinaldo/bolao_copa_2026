import streamlit as st
from services.sheets import buscar_usuario


def login(usuario, senha):
    user = buscar_usuario(usuario)

    if not user:
        return False

    if str(user["senha"]) != senha:
        return False

    st.session_state.logado = True
    st.session_state.usuario_id = user["id"]
    st.session_state.usuario = user["usuario"]
    st.session_state.nome = user["nome"]

    return True


def logout():
    st.session_state.logado = False
    st.session_state.usuario_id = None
    st.session_state.usuario = None
    st.session_state.nome = None