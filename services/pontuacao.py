def calcular_pontos_palpite(
    palpite_a,
    palpite_b,
    resultado_a,
    resultado_b,
    gols_jogador=0
):

    pontos = 0

    # Placar exato
    if (
        int(palpite_a) == int(resultado_a)
        and int(palpite_b) == int(resultado_b)
    ):
        pontos += 3

    else:

        vencedor_palpite = (
            1
            if int(palpite_a) > int(palpite_b)
            else 2
            if int(palpite_b) > int(palpite_a)
            else 0
        )

        vencedor_resultado = (
            1
            if int(resultado_a) > int(resultado_b)
            else 2
            if int(resultado_b) > int(resultado_a)
            else 0
        )

        # Acertou vencedor ou empate
        if vencedor_palpite == vencedor_resultado:
            pontos += 1

    # Bônus por gols do jogador apostado
    pontos += int(gols_jogador)

    return pontos

from services.sheets import (
    listar_usuarios,
    listar_todos_palpites,
    listar_jogos,
    listar_gols
)


def calcular_ranking():

    usuarios = listar_usuarios()
    palpites = listar_todos_palpites()
    jogos = listar_jogos()
    gols = listar_gols()

    jogos_por_id = {
        str(jogo["id"]): jogo
        for jogo in jogos
    }

    gols_por_chave = {
        (
            str(gol["jogo_id"]),
            str(gol["jogador_id"])
        ): int(gol["gols"])
        for gol in gols
    }

    ranking = []

    for usuario in usuarios:

        pontos_usuario = 0

        palpites_usuario = [
            palpite
            for palpite in palpites
            if str(palpite["usuario_id"])
            == str(usuario["id"])
        ]

        for palpite in palpites_usuario:

            jogo = jogos_por_id.get(
                str(palpite["jogo_id"])
            )

            if not jogo:
                continue

            if str(jogo["encerrado"]).lower() != "true":
                continue

            gols_jogador = gols_por_chave.get(
                (
                    str(jogo["id"]),
                    str(palpite.get("jogador_gol", ""))
                ),
                0
            )

            pontos_usuario += calcular_pontos_palpite(
                palpite["palpite_a"],
                palpite["palpite_b"],
                jogo["gols_a"],
                jogo["gols_b"],
                gols_jogador
            )

        ranking.append({
            "usuario": usuario["nome"],
            "usuario_id": usuario["id"],
            "pontos": pontos_usuario
        })

    ranking.sort(
        key=lambda x: x["pontos"],
        reverse=True
    )

    return ranking


def calcular_ranking_por_data(data_escolhida):

    usuarios = listar_usuarios()
    palpites = listar_todos_palpites()
    jogos = listar_jogos()
    gols = listar_gols()

    jogos_por_id = {
        str(jogo["id"]): jogo
        for jogo in jogos
        if jogo["data_hora"].split(" ")[0] == data_escolhida
    }

    gols_por_chave = {
        (
            str(gol["jogo_id"]),
            str(gol["jogador_id"])
        ): int(gol["gols"])
        for gol in gols
    }

    ranking = []

    for usuario in usuarios:

        pontos_usuario = 0

        palpites_usuario = [
            palpite
            for palpite in palpites
            if str(palpite["usuario_id"]) == str(usuario["id"])
        ]

        for palpite in palpites_usuario:

            jogo = jogos_por_id.get(
                str(palpite["jogo_id"])
            )

            if not jogo:
                continue

            if str(jogo["encerrado"]).lower() != "true":
                continue

            gols_jogador = gols_por_chave.get(
                (
                    str(jogo["id"]),
                    str(palpite.get("jogador_gol", ""))
                ),
                0
            )

            pontos_usuario += calcular_pontos_palpite(
                palpite["palpite_a"],
                palpite["palpite_b"],
                jogo["gols_a"],
                jogo["gols_b"],
                gols_jogador
            )

        ranking.append({
            "usuario": usuario["nome"],
            "nome": usuario["nome"],
            "usuario_id": usuario["id"],
            "pontos": pontos_usuario
        })

    ranking.sort(
        key=lambda x: x["pontos"],
        reverse=True
    )

    return ranking