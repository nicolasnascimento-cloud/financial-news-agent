import os
import requests

API_KEY = os.environ["GROQ_API_KEY"]

URL = "https://api.groq.com/openai/v1/chat/completions"


def gerar_resumo(texto):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Você é um analista financeiro.

Leia as notícias abaixo.

Escreva:

1. Um resumo executivo.
2. Os cinco principais acontecimentos.
3. O sentimento do mercado (Positivo, Neutro ou Negativo).

Notícias:

{texto}
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    resposta = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    resposta.raise_for_status()

    dados = resposta.json()

    return dados["choices"][0]["message"]["content"]
