from services.sqlite import (
    listar_jogos,
    listar_todos_palpites,
    listar_usuarios,
    listar_gols
)

from datetime import datetime

DATA_INICIO_VALIDA = datetime.strptime(
    "12/06/2026",
    "%d/%m/%Y"
)


def calcular_pontos(
    palpite_a,
    palpite_b,
    real_a,
    real_b
):
    if palpite_a == real_a and palpite_b == real_b:
        return 3

    if real_a == real_b and palpite_a == palpite_b:
        return 1

    if real_a > real_b and palpite_a > palpite_b:
        return 1

    if real_a < real_b and palpite_a < palpite_b:
        return 1

    return 0


def gerar_ranking():

    jogos = listar_jogos()
    palpites = listar_todos_palpites()
    usuarios = listar_usuarios()
    gols = listar_gols()

    ranking = {}

    usuarios_por_id = {
        str(usuario["id"]): usuario["nome"]
        for usuario in usuarios
    }

    jogos_encerrados = {
        str(jogo["id"]): jogo
        for jogo in jogos
        if (
            str(jogo["encerrado"]).lower() in ["true", "1"]
            and datetime.strptime(
                jogo["data_hora"].split(" ")[0],
                "%d/%m/%Y"
            ) >= DATA_INICIO_VALIDA
        )
    }

    gols_por_chave = {
        (
            str(gol["jogo_id"]),
            str(gol["jogador_id"])
        ): int(gol["gols"])
        for gol in gols
    }

    for palpite in palpites:

        jogo = jogos_encerrados.get(
            str(palpite["jogo_id"])
        )

        if not jogo:
            continue

        pontos = calcular_pontos(
            int(palpite["palpite_a"]),
            int(palpite["palpite_b"]),
            int(jogo["gols_a"]),
            int(jogo["gols_b"])
        )

        pontos += gols_por_chave.get(
            (
                str(jogo["id"]),
                str(palpite.get("jogador_gol", ""))
            ),
            0
        )

        usuario_id = str(palpite["usuario_id"])

        ranking[usuario_id] = (
            ranking.get(usuario_id, 0)
            + pontos
        )

    resultado = []

    for usuario_id, pontos in ranking.items():

        resultado.append({
            "usuario_id": usuario_id,
            "nome": usuarios_por_id.get(
                usuario_id,
                "Desconhecido"
            ),
            "pontos": pontos
        })

    resultado.sort(
        key=lambda x: x["pontos"],
        reverse=True
    )

    return resultado


def gerar_ranking_por_data(data_escolhida):

    jogos = listar_jogos()
    palpites = listar_todos_palpites()
    usuarios = listar_usuarios()
    gols = listar_gols()

    ranking = {}

    usuarios_por_id = {
        str(usuario["id"]): usuario["nome"]
        for usuario in usuarios
    }

    jogos_da_data = {
        str(jogo["id"]): jogo
        for jogo in jogos
        if (
            jogo["data_hora"].split(" ")[0] == data_escolhida
            and str(jogo["encerrado"]).lower() in ["true", "1"]
            and datetime.strptime(
                jogo["data_hora"].split(" ")[0],
                "%d/%m/%Y"
            ) >= DATA_INICIO_VALIDA
        )
    }

    gols_por_chave = {
        (
            str(gol["jogo_id"]),
            str(gol["jogador_id"])
        ): int(gol["gols"])
        for gol in gols
    }

    for palpite in palpites:

        jogo = jogos_da_data.get(
            str(palpite["jogo_id"])
        )

        if not jogo:
            continue

        pontos = calcular_pontos(
            int(palpite["palpite_a"]),
            int(palpite["palpite_b"]),
            int(jogo["gols_a"]),
            int(jogo["gols_b"])
        )

        pontos += gols_por_chave.get(
            (
                str(jogo["id"]),
                str(palpite.get("jogador_gol", ""))
            ),
            0
        )

        usuario_id = str(palpite["usuario_id"])

        ranking[usuario_id] = (
            ranking.get(usuario_id, 0)
            + pontos
        )

    resultado = []

    for usuario_id, pontos in ranking.items():
        resultado.append({
            "usuario_id": usuario_id,
            "nome": usuarios_por_id.get(
                usuario_id,
                "Desconhecido"
            ),
            "pontos": pontos
        })

    resultado.sort(
        key=lambda x: x["pontos"],
        reverse=True
    )

    return resultado


def gerar_ranking_placares():

    jogos = listar_jogos()
    palpites = listar_todos_palpites()
    usuarios = listar_usuarios()

    usuarios_por_id = {
        str(usuario["id"]): usuario["nome"]
        for usuario in usuarios
    }

    jogos_encerrados = {
        str(jogo["id"]): jogo
        for jogo in jogos
        if (
            str(jogo["encerrado"]).lower() in ["true", "1"]
            and datetime.strptime(
                jogo["data_hora"].split(" ")[0],
                "%d/%m/%Y"
            ) >= DATA_INICIO_VALIDA
        )
    }

    ranking = {}

    for palpite in palpites:

        jogo = jogos_encerrados.get(
            str(palpite["jogo_id"])
        )

        if not jogo:
            continue

        if (
            int(palpite["palpite_a"]) == int(jogo["gols_a"])
            and int(palpite["palpite_b"]) == int(jogo["gols_b"])
        ):

            usuario_id = str(palpite["usuario_id"])

            ranking[usuario_id] = (
                ranking.get(usuario_id, 0) + 1
            )

    resultado = []

    for usuario_id, acertos in ranking.items():

        resultado.append({
            "usuario_id": usuario_id,
            "nome": usuarios_por_id.get(
                usuario_id,
                "Desconhecido"
            ),
            "acertos": acertos
        })

    resultado.sort(
        key=lambda x: x["acertos"],
        reverse=True
    )

    return resultado


def gerar_ranking_artilheiros():

    palpites = listar_todos_palpites()
    usuarios = listar_usuarios()
    gols = listar_gols()
    jogos = listar_jogos()

    jogos_validos = {

        str(jogo["id"])
        for jogo in jogos
        if (
            str(jogo["encerrado"]).lower() in ["true", "1"]
            and datetime.strptime(
                jogo["data_hora"].split(" ")[0],
                "%d/%m/%Y"
            ) >= DATA_INICIO_VALIDA
        )
    }

    usuarios_por_id = {
        str(usuario["id"]): usuario["nome"]
        for usuario in usuarios
    }

    gols_validos = {
        (
            str(gol["jogo_id"]),
            str(gol["jogador_id"])
        )
        for gol in gols
    }

    ranking = {}

    for palpite in palpites:

        chave = (
            str(palpite["jogo_id"]),
            str(palpite.get("jogador_gol", ""))
        )

        if (
            str(palpite["jogo_id"]) in jogos_validos
            and chave in gols_validos
        ):

            usuario_id = str(palpite["usuario_id"])

            ranking[usuario_id] = (
                ranking.get(usuario_id, 0) + 1
            )

    resultado = []

    for usuario_id, acertos in ranking.items():

        resultado.append({
            "usuario_id": usuario_id,
            "nome": usuarios_por_id.get(
                usuario_id,
                "Desconhecido"
            ),
            "acertos": acertos
        })

    resultado.sort(
        key=lambda x: x["acertos"],
        reverse=True
    )

    return resultado



