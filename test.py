import requests
from config import OPENROUTER_API_KEY

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
}

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers=headers
)

models = response.json()["data"]

for m in models:
    print(m["id"])