

from services.db import get_conn
from services.sheets import (
    listar_usuarios,
    listar_jogos,
    listar_jogadores,
    listar_todos_palpites,
    listar_gols
)

conn = get_conn()
cursor = conn.cursor()

print("Migrando usuários...")
for usuario in listar_usuarios():
    cursor.execute(
        """
        INSERT OR REPLACE INTO usuarios
        (id, nome, usuario, senha)
        VALUES (?, ?, ?, ?)
        """,
        (
            int(usuario["id"]),
            usuario["nome"],
            usuario["usuario"],
            usuario["senha"]
        )
    )

print("Migrando jogos...")
for jogo in listar_jogos():
    cursor.execute(
        """
        INSERT OR REPLACE INTO jogos
        (id, data_hora, time_a, time_b, gols_a, gols_b, encerrado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            int(jogo["id"]),
            jogo["data_hora"],
            jogo["time_a"],
            jogo["time_b"],
            int(jogo.get("gols_a", 0) or 0),
            int(jogo.get("gols_b", 0) or 0),
            1 if str(jogo.get("encerrado", "False")).lower() == "true" else 0
        )
    )

print("Migrando jogadores...")
for jogador in listar_jogadores():
    cursor.execute(
        """
        INSERT OR REPLACE INTO jogadores
        (id, selecao, jogador)
        VALUES (?, ?, ?)
        """,
        (
            int(jogador["id"]),
            jogador["selecao"],
            jogador["jogador"]
        )
    )

print("Migrando palpites...")
for palpite in listar_todos_palpites():
    cursor.execute(
        """
        INSERT OR REPLACE INTO palpites
        (usuario_id, jogo_id, palpite_a, palpite_b, atualizado_em, jogador_gol)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            int(palpite["usuario_id"]),
            int(palpite["jogo_id"]),
            int(palpite["palpite_a"]),
            int(palpite["palpite_b"]),
            palpite["atualizado_em"],
            int(palpite.get("jogador_gol", 0) or 0)
        )
    )

print("Migrando gols...")
for gol in listar_gols():
    cursor.execute(
        """
        INSERT OR REPLACE INTO gols
        (id, jogo_id, jogador_id, gols)
        VALUES (?, ?, ?, ?)
        """,
        (
            int(gol["id"]),
            int(gol["jogo_id"]),
            int(gol["jogador_id"]),
            int(gol["gols"])
        )
    )

conn.commit()
conn.close()

print("Migração concluída com sucesso.")