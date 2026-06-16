import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from services.footer import mostrar_rodape


if not st.session_state.get("logado"):
    st.switch_page("Home.py")

from services.sqlite import (
    listar_jogos,
    listar_jogadores,
    obter_palpite,
    salvar_ou_atualizar_palpite,
)


st.title("⚽ Jogos")
modo_mobile = st.session_state.get(
    "modo_mobile",
    False
)
FUSO_HORARIO = ZoneInfo("America/Bahia")


jogos = listar_jogos()

# Datas disponíveis
_datas_disponiveis = sorted(
    list({jogo["data_hora"].split(" ")[0] for jogo in jogos})
)

if _datas_disponiveis:

    hoje = datetime.now().strftime("%d/%m/%Y")

    indice_padrao = 0

    if hoje in _datas_disponiveis:
        indice_padrao = _datas_disponiveis.index(hoje)

    data_selecionada = st.selectbox(
        "📅 Filtrar por data",
        _datas_disponiveis,
        index=indice_padrao
    )

    jogos = [
        jogo
        for jogo in jogos
        if jogo["data_hora"].startswith(data_selecionada)
    ]


for jogo in jogos:
    st.divider()

    st.subheader(
        f'{jogo["time_a"]} x {jogo["time_b"]}'
    )
    st.caption(f'📅 {jogo["data_hora"]}')
    data_jogo = datetime.strptime(
        jogo["data_hora"],
        "%d/%m/%Y %H:%M"
    ).replace(tzinfo=FUSO_HORARIO)
    status_encerrado = (
        str(jogo["encerrado"]).lower() == "true"
    )
    agora = datetime.now(FUSO_HORARIO)
    pode_apostar = (
        agora < data_jogo and not status_encerrado
    )
    if pode_apostar == True:
        st.write("✅ Você pode palpitar, adiante seu baba logo não, fique aí")
    else:
        st.write("❌ Deu mole pvt, acabou o tempo.")

    palpite_existente = obter_palpite(
        st.session_state.usuario_id,
        jogo["id"]
    )

    valor_a = 0
    valor_b = 0
    jogador_salvo = None

    if palpite_existente:
        st.info(
    f'Última atualização: {palpite_existente["atualizado_em"]}'
        )
        valor_a = int(palpite_existente["palpite_a"])
        valor_b = int(palpite_existente["palpite_b"])
        jogador_salvo = palpite_existente.get("jogador_gol")

    if not pode_apostar:

        st.warning("🔒 Palpites encerrados")

        st.write(
            f'Palpite registrado: {jogo["time_a"]} {valor_a} x {valor_b} {jogo["time_b"]}'
        )

    else:

        col1, col2 = st.columns(2)

        with col1:
            palpite_a = st.number_input(
                jogo["time_a"],
                min_value=0,
                value=valor_a,
                key=f'a_{jogo["id"]}'
            )

        with col2:
            palpite_b = st.number_input(
                jogo["time_b"],
                min_value=0,
                value=valor_b,
                key=f'b_{jogo["id"]}'
            )

        todos_jogadores = listar_jogadores()

        indice_time = 0

        if jogador_salvo:
            jogador_salvo_info = next(
                (
                    j for j in todos_jogadores
                    if str(j["id"]) == str(jogador_salvo)
                ),
                None
            )

            if (
                jogador_salvo_info
                and jogador_salvo_info["selecao"] == jogo["time_b"]
            ):
                indice_time = 1

        time_jogador = st.radio(
            "⚽ Time do artilheiro",
            [
                jogo["time_a"],
                jogo["time_b"]
            ],
            index=indice_time,
            horizontal=True,
            key=f'time_jogador_{jogo["id"]}'
        )

        jogadores_disponiveis = [
            jogador
            for jogador in todos_jogadores
            if jogador["selecao"] == time_jogador
        ]

        jogador_options = [
            jogador["id"]
            for jogador in jogadores_disponiveis
        ]

        jogador_index = 0

        if jogador_salvo and jogador_salvo in jogador_options:
            jogador_index = jogador_options.index(jogador_salvo)

        if not modo_mobile:

            jogador_escolhido = st.selectbox(
                "⚽ Jogador",
                options=jogador_options,
                index=jogador_index,
                format_func=lambda jogador_id: next(
                    j["jogador"]
                    for j in jogadores_disponiveis
                    if str(j["id"]) == str(jogador_id)
                ),
                key=f'jogador_{jogo["id"]}'
            )

        else:

            jogador_escolhido = st.radio(
                "⚽ Jogador",
                options=jogador_options,
                index=jogador_index,
                format_func=lambda jogador_id: next(
                    j["jogador"]
                    for j in jogadores_disponiveis
                    if str(j["id"]) == str(jogador_id)
                ),
                key=f'jogador_{jogo["id"]}'
            )

        if st.button(
            "Salvar",
            key=f'salvar_{jogo["id"]}'
        ):
            salvar_ou_atualizar_palpite(
                st.session_state.usuario_id,
                jogo["id"],
                palpite_a,
                palpite_b,
                jogador_escolhido
            )

            st.success("Palpite salvo")
mostrar_rodape()