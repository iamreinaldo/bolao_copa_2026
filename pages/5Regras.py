

import streamlit as st
from services.footer import mostrar_rodape

st.title("📜 Regras do Bolão")

st.markdown(
    """
# 🏆 Como Funciona a Pontuação

Em cada partida você deverá informar:

- Placar do Time A
- Placar do Time B
- Um jogador que você acredita que marcará gol

---

## ⚽ Acertou o Vencedor

Se você acertar apenas o resultado da partida (triunfo, empate ou derrota):

**+ 1 ponto**

### Exemplo

Palpite:
- Brasil 2 x 1 Argentina

Resultado:
- Brasil 3 x 0 Argentina

Você acertou que o Brasil venceu.

✅ 1 ponto

---

## 🎯 Acertou o Placar Exato

Se você acertar exatamente o placar da partida:

**+ 3 pontos**

### Exemplo

Palpite:
- Brasil 2 x 1 Argentina

Resultado:
- Brasil 2 x 1 Argentina

✅ 3 pontos

---

## 👟 Artilheiro Apostado

Além do placar, você escolhe um jogador para marcar gol.

Cada gol marcado pelo jogador escolhido rende:

**+ 1 ponto extra**

### Exemplo

Você apostou em:
- Vinícius Júnior

Resultado:
- Vinícius Júnior marcou 2 gols

✅ +2 pontos extras

---

## 💰 Exemplo Completo

Palpite:
- Brasil 2 x 1 Argentina
- Artilheiro: Vinícius Júnior

Resultado:
- Brasil 2 x 1 Argentina
- Vinícius Júnior marcou 2 gols

Pontuação:

✅ Placar exato = 3 pontos

✅ Artilheiro = 2 pontos

🏆 Total = 5 pontos

---

# 🍺 Barril Dobrado

O Barril Dobrado é uma competição paralela dentro do bolão.

Em vez de considerar toda a Copa, ele considera apenas os jogos de uma única data.

Ou seja:

- Cada dia possui seu próprio ranking.
- Apenas os jogos daquela data são contabilizados.
- O vencedor do dia é o campeão do Barril Dobrado.

### Exemplo

Dia 15/06:

- Jogo 1
- Jogo 2
- Jogo 3

Somente os pontos conquistados nesses jogos contam para o Barril Dobrado daquela data.

---

# 📈 Ranking Geral

O Ranking Geral considera:

- Todos os jogos da competição
- Todos os pontos obtidos com placares
- Todos os pontos obtidos com artilheiros

Ao final da Copa, o participante com mais pontos será o campeão do bolão.

Boa sorte e que os palpites estejam inspirados! 🍀⚽
"""
)
mostrar_rodape()