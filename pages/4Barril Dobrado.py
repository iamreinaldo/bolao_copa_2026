import streamlit as st
from datetime import datetime

from services.sqlite import listar_jogos
from services.ranking import gerar_ranking_por_data

from services.footer import mostrar_rodape

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


hoje = datetime.now().strftime("%d/%m/%Y")

indice_padrao = 0

if hoje in datas:
    indice_padrao = datas.index(hoje)

data_escolhida = st.selectbox(
    "📅 Escolha uma data",
    datas,
    index=indice_padrao
)

ranking = gerar_ranking_por_data(
    data_escolhida
)
ranking = [
    usuario
    for usuario in ranking
    if str(usuario.get("usuario_id")) != "1"
]

st.subheader(
    f"🏆 O Barril dobrado de {data_escolhida} é"
)

if not ranking:
    st.info(
        "Relaxe que não terminou jogo nenhum ainda."
    )
else:

    vencedor = ranking[0]

    st.success(
        f'🍺 Barril Dobrado: {vencedor["nome"]} ({vencedor["pontos"]} pts)'
    )

    st.divider()

    st.subheader("Classificação da rodada")

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

        nome = usuario.get("nome", usuario.get("usuario", "-"))

        st.write(
            f'{medalha} {posicao}º - {nome} ({usuario["pontos"]} pts)'
        )
mostrar_rodape()