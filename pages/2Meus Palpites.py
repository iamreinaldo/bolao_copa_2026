import streamlit as st
from services.footer import mostrar_rodape

if not st.session_state.get("logado"):
    st.switch_page("Home.py")

from services.sqlite import (
    listar_jogos,
    listar_jogadores,
    listar_palpites_usuario
)

st.title("📝 Meus Palpites")

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

if not palpites:
    st.info("Irmão, deixe de ser imbecil, você ainda não realizou nenhum palpite.")
else:
    for palpite in palpites:

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


mostrar_rodape()