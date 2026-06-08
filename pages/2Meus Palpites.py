import streamlit as st

if not st.session_state.get("logado"):
    st.switch_page("Home.py")

from services.sheets import (
    listar_palpites_usuario,
    listar_jogos
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

        st.divider()