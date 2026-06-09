import pdfplumber
import pandas as pd
import re

texto = ""

with pdfplumber.open("SquadLists-English.pdf") as pdf:
    for pagina in pdf.pages:
        pagina_texto = pagina.extract_text()
        if pagina_texto:
            texto += pagina_texto + "\n"

selecao = None
dados = []

for linha in texto.split("\n"):

    linha = linha.strip()

    # Detecta seleção
    m = re.match(r"^(.+?) \([A-Z]{3}\)$", linha)

    if m and "World Cup" not in linha:
        selecao = m.group(1)
        continue

    # Detecta jogador
    m = re.match(
        r"^(\d+)\s+(GK|DF|MF|FW)\s+([A-Z\-\s]+)\s+(.+)$",
        linha
    )

    if m and selecao:

        numero = m.group(1)
        posicao = m.group(2)

        partes = linha.split()

        jogador = " ".join(partes[3:6])

        dados.append({
            "selecao": selecao,
            "numero": numero,
            "posicao": posicao,
            "jogador": jogador
        })

df = pd.DataFrame(dados)

df.to_csv(
    "jogadores.csv",
    index=False,
    encoding="utf-8-sig"
)