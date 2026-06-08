

import streamlit as st

from services.sheets import listar_jogos
from services.ranking import gerar_ranking_por_data

if not st.session_state.get("logado"):
    st.switch_page("Home.py")

st.title("🍺 Barril Dobrado")

jogos = listar_jogos()

if not jogos:
    st.info("Nenhum jogo cadastrado.")
    st.stop()

# Datas cadastradas na planilha
datas = sorted(
    list({
        jogo["data_hora"].split(" ")[0]
        for jogo in jogos
    })
)

data_escolhida = st.selectbox(
    "📅 Escolha uma data",
    datas
)

ranking = gerar_ranking_por_data(
    data_escolhida
)

st.subheader(
    f"🏆 O Barril dobrado de {data_escolhida} é"
)

if not ranking:
    st.info(
        "Relaxe que não terminou jogo nenhum ainda."
    )
else:

    for posicao, usuario in enumerate(
        ranking,
        start=1
    ):

        medalha = ""

        if posicao == 1:
            medalha = "🥇"
        elif posicao == 2:
            medalha = "🥈"
        elif posicao == 3:
            medalha = "🥉"

        st.write(
            f'{medalha} {usuario["nome"]} - {usuario["pontos"]} pts'
        )