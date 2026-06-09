import streamlit as st
from services.footer import mostrar_rodape

if not st.session_state.get("logado"):
    st.switch_page("Home.py")

from services.pontuacao import calcular_ranking

st.title("🏆 Ranking")

ranking = calcular_ranking()

if not ranking:
    st.info("Ainda não existem jogos encerrados.")
else:

    for posicao, usuario in enumerate(ranking, start=1):

        medalha = ""

        if posicao == 1:
            medalha = "🥇"
        elif posicao == 2:
            medalha = "🥈"
        elif posicao == 3:
            medalha = "🥉"

        st.write(
            f'{medalha} {posicao}º - {usuario["usuario"]} ({usuario["pontos"]} pts)'
        )


mostrar_rodape()