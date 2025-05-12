import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CHATPDF_API_KEY")

headers = {
    "x-api-key": api_key
}

# Substitua pelo caminho do seu PDF
file_path = "Consulta/Receitas.pdf"


with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(
        "https://api.chatpdf.com/v1/sources/add-file",
        headers=headers,
        files=files
    )

if response.status_code == 200:
    source_id = response.json()["sourceId"]
    print("✅ Seu SOURCE_ID é:", source_id)
else:
    print("❌ Erro:", response.text)
