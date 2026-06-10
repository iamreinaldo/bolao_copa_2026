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
from services.sqlite import (
    listar_jogos,
    listar_jogadores,
    listar_usuarios,
    listar_todos_palpites,
    adicionar_jogo,
    editar_jogo,
    criar_usuario,
    atualizar_usuario,
    excluir_usuario,
    atualizar_resultado,
    salvar_ou_atualizar_gol,
    buscar_gols_jogador,
    adicionar_jogador,
    editar_jogador,
    excluir_jogador
)

st.title("⚙️ Administração")

aba_jogos, aba_resultados, aba_usuarios, aba_jogadores, aba_palpites, aba_pendentes = st.tabs([
    "➕ Jogos",
    "🏁 Resultados",
    "👤 Usuários",
    "⚽ Jogadores",
    "📝 Palpites",
    "🚨 Pendentes"
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

    st.header("✏️ Editar Jogos")

    jogos = listar_jogos()

    datas_jogos = sorted(
        list({
            jogo["data_hora"].split(" ")[0]
            for jogo in jogos
        })
    )

    if datas_jogos:

        data_edicao = st.selectbox(
            "📅 Data dos jogos",
            datas_jogos,
            key="data_edicao_jogos"
        )

        jogos_filtrados = [
            jogo
            for jogo in jogos
            if jogo["data_hora"].startswith(data_edicao)
        ]

        if jogos_filtrados:

            jogo_selecionado = st.selectbox(
                "⚽ Jogo",
                jogos_filtrados,
                format_func=lambda j: f'{j["time_a"]} x {j["time_b"]}',
                key="jogo_edicao"
            )

            data_hora_edicao = st.text_input(
                "Data e Hora",
                value=jogo_selecionado["data_hora"],
                key=f'editar_data_hora_{jogo_selecionado["id"]}'
            )

            col_ed1, col_ed2 = st.columns(2)

            with col_ed1:
                time_a_edicao = st.selectbox(
                    "Time A",
                    SELECOES,
                    index=SELECOES.index(jogo_selecionado["time_a"]),
                    key=f'editar_time_a_{jogo_selecionado["id"]}'
                )

            with col_ed2:
                time_b_edicao = st.selectbox(
                    "Time B",
                    SELECOES,
                    index=SELECOES.index(jogo_selecionado["time_b"]),
                    key=f'editar_time_b_{jogo_selecionado["id"]}'
                )

            if st.button(
                "Salvar Jogo",
                key="salvar_jogo_editado"
            ):
                try:
                    datetime.strptime(
                        data_hora_edicao,
                        "%d/%m/%Y %H:%M"
                    )
                except ValueError:
                    st.error("Use o formato DD/MM/AAAA HH:MM")
                    st.stop()

                if time_a_edicao == time_b_edicao:
                    st.error("Os times devem ser diferentes")
                    st.stop()

                editar_jogo(
                    jogo_selecionado["id"],
                    data_hora_edicao,
                    time_a_edicao,
                    time_b_edicao
                )

                st.success("Jogo atualizado com sucesso.")
                st.rerun()

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

        senha = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=8
            )
        )

        criar_usuario(
            nome,
            usuario,
            senha
        )

        st.success("Usuário criado")

        st.code(
            f"Usuário: {usuario}\nSenha: {senha}"
        )

    st.divider()

    st.header("✏️ Editar Usuário")

    usuarios = [
        u
        for u in listar_usuarios()
        if int(u["id"]) != 1
    ]

    if usuarios:

        usuario_selecionado = st.selectbox(
            "Selecione o usuário",
            usuarios,
            format_func=lambda u: f'{u["nome"]} ({u["usuario"]})'
        )
        st.session_state["editar_nome"] = usuario_selecionado["nome"]
        st.session_state["editar_senha"] = usuario_selecionado["senha"]

        nome_edicao = st.text_input(
            "Nome",
            key="editar_nome"
        )

        senha_edicao = st.text_input(
            "Senha",
            key="editar_senha"
        )

        if st.button(
            "Salvar Alterações",
            key="salvar_usuario"
        ):

            atualizar_usuario(
                usuario_selecionado["id"],
                nome_edicao,
                senha_edicao
            )

            st.success(
                "Usuário atualizado com sucesso."
            )

            st.rerun()

        st.divider()

        if st.button(
            "🗑️ Excluir Usuário",
            key="excluir_usuario"
        ):

            excluir_usuario(
                usuario_selecionado["id"]
            )

            st.success(
                "Usuário excluído com sucesso."
            )

            st.rerun()
with aba_jogadores:

    st.header("⚽ Gerenciar Jogadores")

    selecao_filtro = st.selectbox(
        "Seleção",
        SELECOES,
        key="selecao_jogadores"
    )

    todos_jogadores = listar_jogadores()

    jogadores_filtrados = [
        j
        for j in todos_jogadores
        if j["selecao"] == selecao_filtro
    ]

    st.subheader("➕ Adicionar Jogador")

    if "novo_jogador_key" not in st.session_state:
        st.session_state["novo_jogador_key"] = 0

    novo_jogador = st.text_input(
        "Nome do jogador",
        key=f"novo_jogador_{st.session_state['novo_jogador_key']}"
    )

    if st.button(
        "Adicionar Jogador",
        key="adicionar_jogador"
    ):

        adicionar_jogador(
            selecao_filtro,
            novo_jogador
        )

        st.session_state["novo_jogador_key"] += 1

        st.success("Jogador adicionado.")
        st.rerun()

    st.divider()

    if jogadores_filtrados:

        jogador_selecionado = st.selectbox(
            "Jogador",
            jogadores_filtrados,
            format_func=lambda j: j["jogador"],
            key="jogador_edicao"
        )

        st.session_state["editar_jogador_nome"] = jogador_selecionado["jogador"]

        nome_jogador = st.text_input(
            "Nome",
            key="editar_jogador_nome"
        )

        if st.button(
            "Salvar Jogador",
            key="salvar_jogador"
        ):

            editar_jogador(
                jogador_selecionado["id"],
                selecao_filtro,
                nome_jogador
            )

            st.success("Jogador atualizado.")
            st.rerun()

        if st.button(
            "🗑️ Excluir Jogador",
            key="excluir_jogador"
        ):

            excluir_jogador(
                jogador_selecionado["id"]
            )

            st.success("Jogador excluído.")
            st.rerun()

with aba_palpites:

    st.header("📝 Todos os Palpites")

    usuarios = {
        str(u["id"]): u
        for u in listar_usuarios()
    }

    jogos = {
        str(j["id"]): j
        for j in listar_jogos()
    }

    jogadores = {
        str(j["id"]): j["jogador"]
        for j in listar_jogadores()
    }

    palpites = listar_todos_palpites()

    usuarios_com_palpites = sorted(
        {
            str(p["usuario_id"])
            for p in palpites
        }
    )

    usuario_id = st.selectbox(
        "👤 Usuário",
        usuarios_com_palpites,
        format_func=lambda uid: usuarios.get(uid, {}).get("nome", uid)
    )

    usuario = usuarios.get(usuario_id)

    if usuario:

        st.subheader(usuario["nome"])

        palpites_usuario = [
            p
            for p in palpites
            if str(p["usuario_id"]) == usuario_id
        ]

        for palpite in palpites_usuario:

            jogo = jogos.get(
                str(palpite["jogo_id"])
            )

            if not jogo:
                continue

            jogador_apostado = jogadores.get(
                str(palpite.get("jogador_gol", "")),
                "Não informado"
            )

            st.write(
                f'{jogo["time_a"]} {palpite["palpite_a"]} x {palpite["palpite_b"]} {jogo["time_b"]}'
            )

            st.caption(
                f'Artilheiro: {jogador_apostado}'
            )

    st.divider()

with aba_pendentes:

    st.header("🚨 Quem Ainda Não Apostou")

    todos_usuarios = [
        u
        for u in listar_usuarios()
        if u["usuario"] != "admin"
    ]

    todos_jogos = listar_jogos()
    todos_palpites = listar_todos_palpites()

    datas = sorted(
        list({
            jogo["data_hora"].split(" ")[0]
            for jogo in todos_jogos
        })
    )

    if datas:

        data_selecionada = st.selectbox(
            "📅 Data",
            datas,
            key="data_pendentes"
        )

        jogos_data = [
            jogo
            for jogo in todos_jogos
            if jogo["data_hora"].startswith(data_selecionada)
        ]

        usuarios_pendentes = []

        for usuario in todos_usuarios:

            possui_todos = True

            for jogo in jogos_data:

                encontrou = any(
                    str(p["usuario_id"]) == str(usuario["id"])
                    and str(p["jogo_id"]) == str(jogo["id"])
                    for p in todos_palpites
                )

                if not encontrou:
                    possui_todos = False
                    break

            if not possui_todos:
                usuarios_pendentes.append(usuario)

        st.subheader(
            f"Pendentes: {len(usuarios_pendentes)}"
        )

        if usuarios_pendentes:
            for usuario in usuarios_pendentes:
                st.write(f"• {usuario['nome']}")
        else:
            st.success("Todos os participantes já apostaram nesta data.")
mostrar_rodape()