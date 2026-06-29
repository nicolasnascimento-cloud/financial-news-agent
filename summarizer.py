import os
import requests

# ==========================
# CONFIGURAÇÕES
# ==========================

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY não encontrada. Verifique os Secrets do GitHub."
    )

URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "llama-3.3-70b-versatile"

# ==========================
# FUNÇÃO PRINCIPAL
# ==========================

def gerar_resumo(texto):

    prompt = f"""
Você é um analista profissional do mercado financeiro brasileiro.

Sua missão é produzir um Morning Brief utilizando EXCLUSIVAMENTE as notícias fornecidas.

REGRAS:

- Nunca invente fatos.
- Nunca faça recomendações de compra ou venda.
- Responda sempre em português.
- Seja objetivo.
- Caso alguma informação esteja repetida, considere apenas uma vez.

Estruture exatamente desta forma:

# 📊 Resumo Executivo

(resumo em até 8 linhas)

# 🔥 Principais acontecimentos

• item 1

• item 2

• item 3

• item 4

• item 5

# 📈 Sentimento do Mercado

Positivo, Neutro ou Negativo.

Explique em até 4 linhas.

# ⚠️ Pontos de Atenção

Liste os principais riscos.

# 💡 Oportunidades

Liste os temas que merecem acompanhamento.

========================

NOTÍCIAS

{texto}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é um analista econômico extremamente experiente."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 1200
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
