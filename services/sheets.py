import gspread
import streamlit as st
from datetime import datetime

import os
import gspread
import streamlit as st

if os.path.exists("data/credentials.json"):
    client = gspread.service_account(
        filename="data/credentials.json"
    )
else:
    client = gspread.service_account_from_dict(
        st.secrets["gcp_service_account"]
    )


# creds = gspread.service_account_from_dict(
#     st.secrets["gcp_service_account"]
# )

# client = gspread.service_account_from_dict(
#     st.secrets["gcp_service_account"]
# )
spreadsheet = client.open("bolao_copa_do_mundo_2026_imbecis")

@st.cache_data(ttl=60)
def listar_usuarios():
    worksheet = spreadsheet.worksheet("usuarios")
    return worksheet.get_all_records()

@st.cache_data(ttl=60)
def listar_todos_palpites():
    worksheet = spreadsheet.worksheet("palpites")
    return worksheet.get_all_records()


def buscar_usuario(usuario):
    worksheet = spreadsheet.worksheet("usuarios")

    usuarios = worksheet.get_all_records()

    for user in usuarios:
        if user["usuario"] == usuario:
            return user
    return None

@st.cache_data(ttl=60)
def listar_jogos():
    worksheet = spreadsheet.worksheet("jogos")
    return worksheet.get_all_records()

def salvar_palpite(
    usuario_id,
    jogo_id,
    palpite_a,
    palpite_b,
    jogador_id
):
    worksheet = spreadsheet.worksheet("palpites")

    worksheet.append_row([
        usuario_id,
        jogo_id,
        palpite_a,
        palpite_b,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        jogador_id
    ])
    st.cache_data.clear()

def buscar_palpite(usuario_id, jogo_id):
    palpites = listar_todos_palpites()

    print(palpites)

    for index, palpite in enumerate(palpites, start=2):
        if (
            str(palpite["usuario_id"]) == str(usuario_id)
            and str(palpite["jogo_id"]) == str(jogo_id)
        ):
            return palpite, index

    return None, None


def salvar_ou_atualizar_palpite(
    usuario_id,
    jogo_id,
    palpite_a,
    palpite_b,
    jogador_id
):
    worksheet = spreadsheet.worksheet("palpites")

    palpite_existente, linha = buscar_palpite(
        usuario_id,
        jogo_id
    )

    if linha:
        worksheet.update(
            f"C{linha}:F{linha}",
            [[
                palpite_a,
                palpite_b,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                jogador_id
            ]]
        )
        st.cache_data.clear()
    else:
        worksheet.append_row([
            usuario_id,
            jogo_id,
            palpite_a,
            palpite_b,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            jogador_id
        ])
        st.cache_data.clear()


def obter_palpite(usuario_id, jogo_id):
    palpites = listar_todos_palpites()

    for palpite in palpites:
        if (
            str(palpite["usuario_id"]) == str(usuario_id)
            and str(palpite["jogo_id"]) == str(jogo_id)
        ):
            return palpite

    return None


@st.cache_data(ttl=60)
def listar_palpites_usuario(usuario_id):
    palpites = listar_todos_palpites()
    return [
        palpite
        for palpite in palpites
        if str(palpite["usuario_id"]) == str(usuario_id)
    ]

def atualizar_resultado(
    jogo_id,
    gols_a,
    gols_b,
    encerrado
):
    worksheet = spreadsheet.worksheet("jogos")

    jogos = worksheet.get_all_records()

    for index, jogo in enumerate(jogos, start=2):

        if str(jogo["id"]) == str(jogo_id):

            worksheet.update(
                f"E{index}:G{index}",
                [[gols_a, gols_b, encerrado]]
            )
            st.cache_data.clear()
            return True

    return False

def adicionar_jogo(
    data_hora,
    time_a,
    time_b
):
    worksheet = spreadsheet.worksheet("jogos")

    jogos = worksheet.get_all_records()

    novo_id = len(jogos) + 1

    worksheet.append_row([
        novo_id,
        data_hora,
        time_a,
        time_b,
        "",
        "",
        False
    ])
    st.cache_data.clear()

@st.cache_data(ttl=60)
def listar_jogadores():
    worksheet = spreadsheet.worksheet("jogadores")
    return worksheet.get_all_records()

@st.cache_data(ttl=60)
def listar_gols():
    worksheet = spreadsheet.worksheet("gols")
    return worksheet.get_all_records()

def adicionar_gol(
    jogo_id,
    jogador_id,
    gols
):
    worksheet = spreadsheet.worksheet("gols")

    registros = worksheet.get_all_records()

    novo_id = (
        max(
            [int(r["id"]) for r in registros],
            default=0
        )
        + 1
    )

    worksheet.append_row([
        novo_id,
        jogo_id,
        jogador_id,
        gols
    ])
    st.cache_data.clear()

def buscar_gols_jogador(
    jogo_id,
    jogador_id
):
    gols = listar_gols()

    for gol in gols:

        if (
            str(gol["jogo_id"]) == str(jogo_id)
            and str(gol["jogador_id"]) == str(jogador_id)
        ):
            return int(gol["gols"])

    return 0


def buscar_gol(
    jogo_id,
    jogador_id
):
    registros = listar_gols()

    for index, gol in enumerate(
        registros,
        start=2
    ):

        if (
            str(gol["jogo_id"]) == str(jogo_id)
            and str(gol["jogador_id"]) == str(jogador_id)
        ):
            return gol, index

    return None, None


def salvar_ou_atualizar_gol(
    jogo_id,
    jogador_id,
    gols
):
    worksheet = spreadsheet.worksheet(
        "gols"
    )

    gol_existente, linha = buscar_gol(
        jogo_id,
        jogador_id
    )

    if linha:
        worksheet.update(
            f"D{linha}",
            [[gols]]
        )
        st.cache_data.clear()

    else:

        registros = worksheet.get_all_records()

        novo_id = (
            max(
                [
                    int(r["id"])
                    for r in registros
                ],
                default=0
            )
            + 1
        )

        worksheet.append_row([
            novo_id,
            jogo_id,
            jogador_id,
            gols
        ])
        st.cache_data.clear()


def adicionar_jogador(
    selecao,
    jogador
):

    worksheet = spreadsheet.worksheet(
        "jogadores"
    )

    registros = worksheet.get_all_records()

    novo_id = (
        max(
            [
                int(r["id"])
                for r in registros
            ],
            default=0
        )
        + 1
    )

    worksheet.append_row([
        novo_id,
        selecao,
        jogador
    ])

    st.cache_data.clear()

    return novo_id

def editar_jogador(
    jogador_id,
    selecao,
    jogador
):

    worksheet = spreadsheet.worksheet(
        "jogadores"
    )

    registros = worksheet.get_all_records()

    for index, registro in enumerate(
        registros,
        start=2
    ):

        if str(registro["id"]) == str(jogador_id):

            worksheet.update(
                f"B{index}:C{index}",
                [[selecao, jogador]]
            )

            st.cache_data.clear()
            return True

    return False



def excluir_jogador(jogador_id):

    worksheet = spreadsheet.worksheet(
        "jogadores"
    )

    registros = worksheet.get_all_records()

    for index, registro in enumerate(
        registros,
        start=2
    ):

        if str(registro["id"]) == str(jogador_id):

            worksheet.delete_rows(index)

            st.cache_data.clear()
            return True

    return False