import requests
from dotenv import load_dotenv
import os

load_dotenv()

def ask_llm(question: str) -> str:
    api_key = os.getenv("API_KEY")
    url = "https://api.deepinfra.com/v1/openai/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "Tu es un assistant utile."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Pour gérer les éventuelles erreurs HTTP proprement
    return response.json()["choices"][0]["message"]["content"]
