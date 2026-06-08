import gspread
import streamlit as st
from datetime import datetime


creds = gspread.service_account_from_dict(
    st.secrets["gcp_service_account"]
)

client = gspread.service_account_from_dict(
    st.secrets["gcp_service_account"]
)
spreadsheet = client.open("bolao_copa_do_mundo_2026_imbecis")

def listar_usuarios():
    worksheet = spreadsheet.worksheet("usuarios")
    return worksheet.get_all_records()


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

def listar_jogos():
    worksheet = spreadsheet.worksheet("jogos")
    return worksheet.get_all_records()

def salvar_palpite(
    usuario_id,
    jogo_id,
    palpite_a,
    palpite_b
):
    worksheet = spreadsheet.worksheet("palpites")

    worksheet.append_row([
        usuario_id,
        jogo_id,
        palpite_a,
        palpite_b,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

def buscar_palpite(usuario_id, jogo_id):
    worksheet = spreadsheet.worksheet("palpites")

    palpites = worksheet.get_all_records()

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
    palpite_b
):
    worksheet = spreadsheet.worksheet("palpites")

    palpite_existente, linha = buscar_palpite(
        usuario_id,
        jogo_id
    )

    if linha:
        worksheet.update(
            f"C{linha}:E{linha}",
            [[
                palpite_a,
                palpite_b,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]]
        )
    else:
        worksheet.append_row([
            usuario_id,
            jogo_id,
            palpite_a,
            palpite_b,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])


def obter_palpite(usuario_id, jogo_id):
    worksheet = spreadsheet.worksheet("palpites")

    palpites = worksheet.get_all_records()

    for palpite in palpites:
        if (
            str(palpite["usuario_id"]) == str(usuario_id)
            and str(palpite["jogo_id"]) == str(jogo_id)
        ):
            return palpite

    return None


def listar_palpites_usuario(usuario_id):
    worksheet = spreadsheet.worksheet("palpites")

    palpites = worksheet.get_all_records()

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