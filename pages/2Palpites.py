import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from services.footer import mostrar_rodape

if not st.session_state.get("logado"):
    st.switch_page("Home.py")

from services.sqlite import (
    listar_jogos,
    listar_jogadores,
    listar_palpites_usuario,
    listar_todos_palpites,
    listar_usuarios
)

st.title("📝 Meus Palpites")
FUSO_HORARIO = ZoneInfo("America/Bahia")

aba_meus_palpites, aba_revelados = st.tabs([
    "📝 Meus Palpites",
    "👀 Palpites Revelados"
])

palpites = listar_palpites_usuario(
    st.session_state.usuario_id
)

jogos = listar_jogos()

jogos_por_id = {
    str(jogo["id"]): jogo
    for jogo in jogos
}

jogadores = listar_jogadores()

jogadores_por_id = {
    str(jogador["id"]): jogador["jogador"]
    for jogador in jogadores
}

with aba_meus_palpites:
    if not palpites:
        st.info("Irmão, deixe de ser imbecil, você ainda não realizou nenhum palpite.")
    else:

        datas_disponiveis = sorted(
            list({
                jogos_por_id[str(p["jogo_id"])] ["data_hora"].split(" ")[0]
                for p in palpites
                if str(p["jogo_id"]) in jogos_por_id
            }),
            key=lambda data: datetime.strptime(data, "%d/%m/%Y")
        )

        data_selecionada = st.selectbox(
            "📅 Data",
            datas_disponiveis,
            key="data_meus_palpites"
        )

        palpites_filtrados = [
            p
            for p in palpites
            if (
                str(p["jogo_id"]) in jogos_por_id
                and jogos_por_id[str(p["jogo_id"])] ["data_hora"].startswith(data_selecionada)
            )
        ]

        for palpite in palpites_filtrados:

            jogo = jogos_por_id.get(
                str(palpite["jogo_id"])
            )

            if not jogo:
                continue

            st.write(
                f'⚽ {jogo["time_a"]} {palpite["palpite_a"]} x {palpite["palpite_b"]} {jogo["time_b"]}'
            )

            st.caption(
                f'Atualizado em: {palpite["atualizado_em"]}'
            )

            jogador_apostado = jogadores_por_id.get(
                str(palpite.get("jogador_gol", "")),
                "Não informado"
            )

            st.caption(
                f'⚽ Artilheiro apostado: {jogador_apostado}'
            )

            st.divider()

with aba_revelados:
    usuarios = {
        str(u["id"]): u["nome"]
        for u in listar_usuarios()
    }

    palpites_todos = listar_todos_palpites()

    jogos_encerrados_para_revelar = []

    for jogo in jogos:

        try:
            data_jogo = datetime.strptime(
                str(jogo["data_hora"]),
                "%d/%m/%Y %H:%M"
            ).replace(tzinfo=FUSO_HORARIO)

            if datetime.now(FUSO_HORARIO) >= data_jogo:
                jogos_encerrados_para_revelar.append(jogo)

        except Exception:
            pass

    datas_disponiveis = sorted(
        list({
            jogo["data_hora"].split(" ")[0]
            for jogo in jogos_encerrados_para_revelar
        }),
        key=lambda data: datetime.strptime(data, "%d/%m/%Y")
    )

    if not datas_disponiveis:
        st.info("Nenhum jogo disponível para revelar palpites.")
        st.stop()

    
    hoje  = datetime.now(FUSO_HORARIO).strftime("%d/%m/%Y")
    indice_padrao = 0

    if hoje in datas_disponiveis:
        indice_padrao = datas_disponiveis.index(hoje)

    data_selecionada = st.selectbox(
        "📅 Data",
        datas_disponiveis,
        index=indice_padrao,
        key="data_palpites_revelados"
    )

    jogos_filtrados = [
        jogo
        for jogo in jogos_encerrados_para_revelar
        if jogo["data_hora"].startswith(data_selecionada)
    ]

    for jogo in jogos_filtrados:

        st.subheader(
            f'{jogo["time_a"]} x {jogo["time_b"]}'
        )

        palpites_jogo = [
            p
            for p in palpites_todos
            if str(p["jogo_id"]) == str(jogo["id"])
        ]

        if not palpites_jogo:
            st.caption("Nenhum palpite registrado.")
            continue

        for palpite in palpites_jogo:

            nome_usuario = usuarios.get(
                str(palpite["usuario_id"]),
                "Usuário"
            )

            jogador_apostado = jogadores_por_id.get(
                str(palpite.get("jogador_gol", "")),
                "Não informado"
            )

            st.write(
                f'**{nome_usuario}** → {palpite["palpite_a"]} x {palpite["palpite_b"]}'
            )

            st.caption(
                f'Artilheiro: {jogador_apostado}'
            )

        st.divider()

    mostrar_rodape()