import streamlit as st
from config.selecoes import SELECOES
from datetime import datetime
if st.session_state.usuario != "admin":

    st.title("Você é admin, painho? 🤨")
    st.image(
        "koao_supremo_lider.jpeg",
        use_container_width=True
    )


    st.stop()
from services.sheets import (
    listar_jogos,
    atualizar_resultado,
    adicionar_jogo,
    listar_usuarios
)

st.title("⚙️ Administração")

aba_jogos, aba_resultados, aba_usuarios = st.tabs([
    "➕ Cadastrar Jogos",
    "🏁 Resultados",
    "👤 Usuários"
])

with aba_jogos:
    st.header("➕ Novo Jogo")

    col1, col2, col3 = st.columns(3)

    with col1:
        data_hora = st.text_input(
            "Data e Hora",
            placeholder="11/06/2026 15:00"
        )

    with col2:
        time_a = st.selectbox(
            "Time A",
            SELECOES,
            key="time_a"
        )
    with col3:
        time_b = st.selectbox(
            "Time B",
            SELECOES,
            key="time_b"
        )

    if st.button("Adicionar Jogo"):

        # Validação de formato de data/hora
        try:
            datetime.strptime(
                data_hora,
                "%d/%m/%Y %H:%M"
            )
        except ValueError:
            st.error(
                "Use o formato DD/MM/AAAA HH:MM"
            )
            st.stop()

        if data_hora and time_a and time_b:
            if time_a == time_b:
                st.error("Os times devem ser diferentes")
                st.stop()
            adicionar_jogo(
                data_hora,
                time_a,
                time_b
            )

            st.success("Jogo adicionado")
            st.rerun()
        else:
            st.error("Preencha todos os campos")

    st.divider()

with aba_resultados:
    jogos = listar_jogos()

    for jogo in jogos:

        st.subheader(
            f'{jogo["time_a"]} x {jogo["time_b"]}'
        )

        st.caption(
            f'📅 {jogo["data_hora"]}'
        )

        col1, col2 = st.columns(2)

        with col1:
            gols_a = st.number_input(
                jogo["time_a"],
                min_value=0,
                value=int(jogo["gols_a"] or 0),
                key=f'gols_a_{jogo["id"]}'
            )

        with col2:
            gols_b = st.number_input(
                jogo["time_b"],
                min_value=0,
                value=int(jogo["gols_b"] or 0),
                key=f'gols_b_{jogo["id"]}'
            )

        encerrado = st.checkbox(
            "Jogo encerrado",
            value=str(jogo["encerrado"]).lower() == "true",
            key=f'encerrado_{jogo["id"]}'
        )

        if st.button(
            "Salvar Resultado",
            key=f'salvar_resultado_{jogo["id"]}'
        ):

            atualizar_resultado(
                jogo["id"],
                gols_a,
                gols_b,
                encerrado
            )

            st.success("Resultado atualizado")

        st.divider()

# Usuários tab
with aba_usuarios:

    st.header("👤 Novo Usuário")

    nome = st.text_input(
        "Nome",
        key="novo_nome"
    )

    usuario = st.text_input(
        "Usuário",
        key="novo_usuario"
    )

    if st.button(
        "Gerar Usuário",
        key="gerar_usuario"
    ):

        import random
        import string
        import gspread
        from services.sheets import spreadsheet

        senha = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=8
            )
        )

        usuarios = listar_usuarios()

        novo_id = 2

        if usuarios:
            novo_id = (
                max(
                    int(u["id"])
                    for u in usuarios
                ) + 1
            )

        worksheet = spreadsheet.worksheet(
            "usuarios"
        )

        worksheet.append_row([
            novo_id,
            nome,
            usuario,
            senha
        ])

        st.success("Usuário criado")

        st.code(
            f"Usuário: {usuario}\nSenha: {senha}"
        )