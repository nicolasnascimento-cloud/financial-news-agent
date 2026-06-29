import os
import smtplib
import feedparser

from email.mime.text import MIMEText
from datetime import datetime

from summarizer import gerar_resumo

# ==========================
# CONFIGURAÇÃO DOS FEEDS
# ==========================

FEEDS = {
    "InfoMoney": "https://www.infomoney.com.br/feed/",
    "Money Times": "https://www.moneytimes.com.br/feed/"
}

# ==========================
# CATEGORIAS
# ==========================

CATEGORIAS = {
    "📈 Bolsa": [
        "ibovespa",
        "ações",
        "acao",
        "b3",
        "petrobras",
        "vale"
    ],

    "💵 Dólar": [
        "dólar",
        "dolar",
        "câmbio",
        "cambio",
        "usd"
    ],

    "🏦 Juros": [
        "selic",
        "copom",
        "juros"
    ],

    "🌎 Internacional": [
        "eua",
        "fed",
        "china",
        "europa"
    ],

    "₿ Cripto": [
        "bitcoin",
        "ethereum",
        "cripto"
    ]
}

# ==========================
# COLETA DAS NOTÍCIAS
# ==========================

noticias = []
titulos = set()

for fonte, url in FEEDS.items():

    feed = feedparser.parse(url)

    for item in feed.entries[:15]:

        titulo = item.title.strip()

        chave = titulo.lower()

        if chave in titulos:
            continue

        titulos.add(chave)

        categoria = "🏢 Empresas"

        for nome_categoria, palavras in CATEGORIAS.items():

            encontrou = False

            for palavra in palavras:

                if palavra in chave:
                    categoria = nome_categoria
                    encontrou = True
                    break

            if encontrou:
                break

        noticias.append({
            "titulo": titulo,
            "fonte": fonte,
            "categoria": categoria,
            "link": item.link
        })

# ==========================
# TESTE DA IA
# ==========================

texto_teste = """
Petrobras anunciou aumento da produção.

O Ibovespa fechou em alta.

O dólar caiu frente ao real.
"""

print("Consultando a Groq...")

resumo_ia = gerar_resumo(texto_teste)

print(resumo_ia)

# ==========================
# ORGANIZAÇÃO
# ==========================

ordem = [
    "📈 Bolsa",
    "💵 Dólar",
    "🏦 Juros",
    "🌎 Internacional",
    "₿ Cripto",
    "🏢 Empresas"
]

# ==========================
# HTML
# ==========================

html = f"""
<html>

<body style="font-family:Arial">

<h1>📊 Resumo Diário do Mercado</h1>

<p>
Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}
</p>

<hr>

<h2>🤖 Resumo gerado pela IA</h2>

<pre style="white-space: pre-wrap; font-family: Arial;">
{resumo_ia}
</pre>

<hr>

"""

for categoria in ordem:

    html += f"<h2>{categoria}</h2>"

    lista = []

    for noticia in noticias:

        if noticia["categoria"] == categoria:
            lista.append(noticia)

    if len(lista) == 0:

        html += "<p>Nenhuma notícia encontrada.</p>"

        continue

    for noticia in lista:

        html += f"""
        <div style="margin-bottom:18px">

        <b>{noticia['titulo']}</b><br>

        Fonte: {noticia['fonte']}<br>

        <a href="{noticia['link']}">
        Ler notícia
        </a>

        </div>
        """

html += """

<hr>

<p style="font-size:12px;color:gray">
Financial Intelligence Agent - V3
</p>

</body>

</html>

"""

# ==========================
# ENVIO DO EMAIL
# ==========================

EMAIL = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
DESTINO = os.environ["DESTINO"]

msg = MIMEText(html, "html")

msg["Subject"] = "📊 Morning Brief (Teste Groq)"

msg["From"] = EMAIL

msg["To"] = DESTINO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

    server.login(EMAIL, EMAIL_PASSWORD)

    server.send_message(msg)

print("Email enviado com sucesso!")
