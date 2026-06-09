import streamlit as st
from config.selecoes import SELECOES
from datetime import datetime
from services.footer import mostrar_rodape

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
    listar_usuarios,
    listar_jogadores,
    salvar_ou_atualizar_gol,
    buscar_gols_jogador
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
    todos_jogadores = listar_jogadores()

    datas_disponiveis = sorted(
        list({
            jogo["data_hora"].split(" ")[0]
            for jogo in jogos
        })
    )

    if datas_disponiveis:

        data_selecionada = st.selectbox(
            "📅 Filtrar por data",
            datas_disponiveis,
            key="admin_data_resultados"
        )

        jogos = [
            jogo
            for jogo in jogos
            if jogo["data_hora"].startswith(
                data_selecionada
            )
        ]

    for jogo in jogos:

        st.divider()

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

        st.markdown("### ⚽ Gols da Partida")


        jogadores_partida = [
            jogador
            for jogador in todos_jogadores
            if (
                jogador["selecao"] == jogo["time_a"]
                or jogador["selecao"] == jogo["time_b"]
            )
        ]

        quantidade_linhas = st.number_input(
            "Quantidade de artilheiros",
            min_value=0,
            max_value=20,
            value=0,
            key=f'qtde_gols_{jogo["id"]}'
        )

        gols_jogadores = {}

        for indice in range(quantidade_linhas):

            col_time, col_jogador, col_gols = st.columns([2, 4, 1])

            with col_time:
                selecao_escolhida = st.selectbox(
                    f'Time #{indice + 1}',
                    [
                        jogo["time_a"],
                        jogo["time_b"]
                    ],
                    key=f'time_gol_{jogo["id"]}_{indice}'
                )

            jogadores_selecao = [
                j
                for j in jogadores_partida
                if j["selecao"] == selecao_escolhida
            ]

            with col_jogador:
                jogador_id = st.selectbox(
                    f'Jogador #{indice + 1}',
                    options=[j["id"] for j in jogadores_selecao],
                    format_func=lambda x: next(
                        j["jogador"]
                        for j in jogadores_selecao
                        if j["id"] == x
                    ),
                    key=f'jogador_{jogo["id"]}_{indice}'
                )

            with col_gols:
                gols = st.number_input(
                    'Gols',
                    min_value=1,
                    value=1,
                    key=f'gols_{jogo["id"]}_{indice}'
                )

            gols_jogadores[jogador_id] = gols

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

            for jogador_id, gols in gols_jogadores.items():

                if gols > 0:
                    salvar_ou_atualizar_gol(
                        jogo["id"],
                        jogador_id,
                        gols
                    )

            st.success("Resultado atualizado")

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
mostrar_rodape()