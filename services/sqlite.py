from services.db import get_conn

def listar_jogos():

    conn = get_conn()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM jogos
        ORDER BY data_hora
    """)

    jogos = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return jogos


def listar_jogadores():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jogadores
        ORDER BY selecao, jogador
        """
    )

    jogadores = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return jogadores


def obter_palpite(
    usuario_id,
    jogo_id
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM palpites
        WHERE usuario_id = ?
        AND jogo_id = ?
        LIMIT 1
        """,
        (usuario_id, jogo_id)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return dict(resultado)

    return None


def salvar_ou_atualizar_palpite(
    usuario_id,
    jogo_id,
    palpite_a,
    palpite_b,
    jogador_id
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO palpites
        (
            usuario_id,
            jogo_id,
            palpite_a,
            palpite_b,
            atualizado_em,
            jogador_gol
        )
        VALUES (?, ?, ?, ?, datetime('now'), ?)
        ON CONFLICT(usuario_id, jogo_id)
        DO UPDATE SET
            palpite_a = excluded.palpite_a,
            palpite_b = excluded.palpite_b,
            atualizado_em = excluded.atualizado_em,
            jogador_gol = excluded.jogador_gol
        """,
        (
            usuario_id,
            jogo_id,
            palpite_a,
            palpite_b,
            jogador_id
        )
    )

    conn.commit()
    conn.close()


def listar_palpites_usuario(usuario_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM palpites
        WHERE usuario_id = ?
        ORDER BY jogo_id
        """,
        (usuario_id,)
    )

    palpites = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return palpites


# New functions
def listar_usuarios():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        ORDER BY nome
        """
    )

    usuarios = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return usuarios


def buscar_usuario(usuario, senha):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE usuario = ?
        AND senha = ?
        LIMIT 1
        """,
        (usuario, senha)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return dict(resultado)

    return None


def criar_usuario(
    nome,
    usuario,
    senha
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios
        (
            nome,
            usuario,
            senha
        )
        VALUES (?, ?, ?)
        """,
        (
            nome,
            usuario,
            senha
        )
    )

    conn.commit()
    conn.close()



def buscar_usuario_por_id(usuario_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE id = ?
        LIMIT 1
        """,
        (usuario_id,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return dict(resultado)

    return None


def atualizar_usuario(
    usuario_id,
    nome,
    senha
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET
            nome = ?,
            senha = ?
        WHERE id = ?
        """,
        (
            nome,
            senha,
            usuario_id
        )
    )

    conn.commit()
    conn.close()


# New function to delete user by id
def excluir_usuario(usuario_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM usuarios
        WHERE id = ?
        """,
        (usuario_id,)
    )

    conn.commit()
    conn.close()


# New functions
def adicionar_jogo(
    data_hora,
    time_a,
    time_b
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jogos
        (
            data_hora,
            time_a,
            time_b,
            gols_a,
            gols_b,
            encerrado
        )
        VALUES (?, ?, ?, 0, 0, 0)
        """,
        (
            data_hora,
            time_a,
            time_b
        )
    )

    conn.commit()
    conn.close()

def editar_jogo(
    jogo_id,
    data_hora,
    time_a,
    time_b
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jogos
        SET
            data_hora = ?,
            time_a = ?,
            time_b = ?
        WHERE id = ?
        """,
        (
            data_hora,
            time_a,
            time_b,
            jogo_id
        )
    )

    conn.commit()
    conn.close()


def atualizar_resultado(
    jogo_id,
    gols_a,
    gols_b,
    encerrado
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jogos
        SET
            gols_a = ?,
            gols_b = ?,
            encerrado = ?
        WHERE id = ?
        """,
        (
            gols_a,
            gols_b,
            1 if encerrado else 0,
            jogo_id
        )
    )

    conn.commit()
    conn.close()


def listar_todos_palpites():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM palpites
        """
    )

    palpites = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return palpites


def listar_gols():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM gols
        """
    )

    gols = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return gols


def buscar_gol(
    jogo_id,
    jogador_id
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM gols
        WHERE jogo_id = ?
        AND jogador_id = ?
        LIMIT 1
        """,
        (jogo_id, jogador_id)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return dict(resultado)

    return None



def salvar_ou_atualizar_gol(
    jogo_id,
    jogador_id,
    quantidade_gols
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO gols
        (
            jogo_id,
            jogador_id,
            gols
        )
        VALUES (?, ?, ?)
        ON CONFLICT(jogo_id, jogador_id)
        DO UPDATE SET
            gols = excluded.gols
        """,
        (
            jogo_id,
            jogador_id,
            quantidade_gols
        )
    )

    conn.commit()
    conn.close()



def buscar_gols_jogador(
    jogo_id,
    jogador_id
):

    gol = buscar_gol(
        jogo_id,
        jogador_id
    )

    if gol:
        return int(gol["gols"])

    return 0


# Novas funções para manipulação de jogadores
def adicionar_jogador(
    selecao,
    jogador
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jogadores
        (
            selecao,
            jogador
        )
        VALUES (?, ?)
        """,
        (
            selecao,
            jogador
        )
    )

    conn.commit()
    conn.close()


def editar_jogador(
    jogador_id,
    selecao,
    jogador
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jogadores
        SET
            selecao = ?,
            jogador = ?
        WHERE id = ?
        """,
        (
            selecao,
            jogador,
            jogador_id
        )
    )

    conn.commit()
    conn.close()


def excluir_jogador(jogador_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM jogadores
        WHERE id = ?
        """,
        (jogador_id,)
    )

    conn.commit()
    conn.close()

def excluir_jogo(jogo_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM gols
        WHERE jogo_id = ?
        """,
        (jogo_id,)
    )

    cursor.execute(
        """
        DELETE FROM palpites
        WHERE jogo_id = ?
        """,
        (jogo_id,)
    )

    cursor.execute(
        """
        DELETE FROM jogos
        WHERE id = ?
        """,
        (jogo_id,)
    )

    conn.commit()
    conn.close()