import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "qwen3:4b",
    "stream": False,
    "messages": [
        {
            "role": "user",
            "content": "Merhaba! Kendini Türkçe tanıt."
        }
    ]
}

response = requests.post(url, json=payload, timeout=180)
response.raise_for_status()

data = response.json()

print(data["message"]["content"])