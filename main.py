import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

FEEDS = {
    "InfoMoney": "https://www.infomoney.com.br/feed/",
    "Money Times": "https://www.moneytimes.com.br/feed/"
}

noticias = []

for fonte, url in FEEDS.items():
    try:
        feed = feedparser.parse(url)

        for item in feed.entries[:10]:
            noticias.append({
                "fonte": fonte,
                "titulo": item.title,
                "link": item.link
            })

    except Exception as e:
        print(f"Erro ao ler {fonte}: {e}")

html = f"""
<html>
<body>
<h1>Resumo Diário do Mercado</h1>
<p>Data: {datetime.now().strftime('%d/%m/%Y')}</p>
"""

for noticia in noticias:
    html += f"""
    <p>
        <b>{noticia['titulo']}</b><br>
        Fonte: {noticia['fonte']}<br>
        <a href="{noticia['link']}">Ler notícia</a>
    </p>
    <hr>
    """

html += "</body></html>"

EMAIL = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
DESTINO = os.environ["DESTINO"]

msg = MIMEText(html, "html")
msg["Subject"] = "Resumo Diário Mercado Financeiro"
msg["From"] = EMAIL
msg["To"] = DESTINO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)

print("Email enviado com sucesso!")
