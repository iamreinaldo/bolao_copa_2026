import streamlit as st
from datetime import datetime

from services.sqlite import listar_jogos
from services.ranking import gerar_ranking_por_data, gerar_ranking_placares, gerar_ranking_artilheiros


from services.footer import mostrar_rodape

if not st.session_state.get("logado"):
    st.switch_page("Home.py")

st.title("🍺 Barril Dobrado")
aba_ranking, aba_estatisticas = st.tabs(
    [
        "🍺 Ranking da Rodada",
        "📊 Estatísticas"
    ]
)

jogos = listar_jogos()

if not jogos:
    st.info("Nenhum jogo cadastrado.")
    st.stop()

# Datas cadastradas na planilha
datas = sorted(
    list({
        jogo["data_hora"].split(" ")[0]
        for jogo in jogos
    }),
    key=lambda data: datetime.strptime(data, "%d/%m/%Y")
)
hoje = datetime.now().strftime("%d/%m/%Y")

indice_padrao = 0

if hoje in datas:
    indice_padrao = datas.index(hoje)

with aba_ranking:
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

with aba_estatisticas:
    st.subheader("📊 Estatísticas Barril")

    st.markdown("### 🎯 Ranking de Placares Exatos")

    ranking_placares = gerar_ranking_placares()

    if not ranking_placares:
        st.info("Nenhum placar exato até o momento.")
    else:

        for posicao, usuario in enumerate(
            ranking_placares,
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
                f'{medalha} {posicao}º - {usuario["nome"]} ({usuario["acertos"]})'
            )

    st.divider()

    st.markdown("### ⚽ Ranking de Artilheiros Acertados")

    ranking_artilheiros = gerar_ranking_artilheiros()

    if not ranking_artilheiros:
        st.info("Nenhum artilheiro acertado até o momento.")
    else:

        for posicao, usuario in enumerate(
            ranking_artilheiros,
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
                f'{medalha} {posicao}º - {usuario["nome"]} ({usuario["acertos"]})'
            )

mostrar_rodape()