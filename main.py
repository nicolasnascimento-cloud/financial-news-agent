import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

FEEDS = {
"InfoMoney": "https://www.infomoney.com.br/feed/",
"Money Times": "https://www.moneytimes.com.br/feed/"
}

categorias = {
"📈 Bolsa": ["ibovespa", "ações", "bolsa", "b3"],
"💵 Dólar": ["dólar", "câmbio", "usd"],
"🏦 Juros": ["selic", "copom", "juros"],
"🌎 Internacional": ["eua", "fed", "china", "europa"],
"₿ Cripto": ["bitcoin", "ethereum", "cripto"],
}

noticias_unicas = []
titulos_vistos = set()

for fonte, url in FEEDS.items():

```
feed = feedparser.parse(url)

for item in feed.entries[:15]:

    titulo = item.title.strip()

    titulo_normalizado = titulo.lower()

    if titulo_normalizado in titulos_vistos:
        continue

    titulos_vistos.add(titulo_normalizado)

    categoria = "🏢 Empresas"

    for cat, palavras in categorias.items():
        if any(p in titulo_normalizado for p in palavras):
            categoria = cat
            break

    noticias_unicas.append({
        "fonte": fonte,
        "titulo": titulo,
        "link": item.link,
        "categoria": categoria
    })
```

html = f"""

<html>
<body style="font-family:Arial">

<h1>📊 Resumo Diário do Mercado</h1>

<p>
Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}
</p>

"""

for categoria in [
"📈 Bolsa",
"💵 Dólar",
"🏦 Juros",
"🌎 Internacional",
"₿ Cripto",
"🏢 Empresas"
]:

```
html += f"<h2>{categoria}</h2>"

categoria_noticias = [
    n for n in noticias_unicas
    if n["categoria"] == categoria
]

if not categoria_noticias:
    html += "<p>Nenhuma notícia encontrada.</p>"
    continue

for noticia in categoria_noticias:

    html += f"""
    <div style='margin-bottom:15px'>
        <b>{noticia["titulo"]}</b><br>
        Fonte: {noticia["fonte"]}<br>
        <a href='{noticia["link"]}'>
            Ler notícia
        </a>
    </div>
    """
```

html += "</body></html>"

EMAIL = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
DESTINO = os.environ["DESTINO"]

msg = MIMEText(html, "html")
msg["Subject"] = "📊 Resumo Diário Mercado Financeiro"
msg["From"] = EMAIL
msg["To"] = DESTINO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
server.login(EMAIL, EMAIL_PASSWORD)
server.send_message(msg)

print("Email enviado com sucesso!")
