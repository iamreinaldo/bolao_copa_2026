import sqlite3

conn = sqlite3.connect("data/bolao.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY,
    data_hora TEXT NOT NULL,
    time_a TEXT NOT NULL,
    time_b TEXT NOT NULL,
    gols_a INTEGER,
    gols_b INTEGER,
    encerrado INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS jogadores (
    id INTEGER PRIMARY KEY,
    selecao TEXT NOT NULL,
    jogador TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS palpites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    jogo_id INTEGER NOT NULL,
    palpite_a INTEGER NOT NULL,
    palpite_b INTEGER NOT NULL,
    atualizado_em TEXT NOT NULL,
    jogador_gol INTEGER,
    UNIQUE(usuario_id, jogo_id)
);

CREATE TABLE IF NOT EXISTS gols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER NOT NULL,
    jogador_id INTEGER NOT NULL,
    gols INTEGER NOT NULL,
    UNIQUE(jogo_id, jogador_id)
);
""")

conn.commit()
conn.close()

print("Banco SQLite criado com sucesso.")