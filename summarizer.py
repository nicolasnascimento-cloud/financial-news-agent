import os
import requests

URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "llama-3.3-70b-versatile"

API_KEY = os.environ["GROQ_API_KEY"]


def gerar_resumo(texto):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é um analista financeiro."
            },
            {
                "role": "user",
                "content": texto
            }
        ],
        "temperature": 0.2
    }

    resposta = requests.post(
        URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    resposta.raise_for_status()

    dados = resposta.json()

    return dados["choices"][0]["message"]["content"]
