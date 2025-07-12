import requests
import base64
import json
from config import OPENAI_API_KEY

def analyze_image_with_gpt(image_path):
    with open(image_path, "rb") as img:
        base64_image = base64.b64encode(img.read()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah AI Trader Gold tahap legenda. Apabila diberi carta, anda perlu beri analisis lengkap mengikut format God++ Mode. Gunakan semua logik teknikal multi-timeframe, candlestick, struktur, dan zon harga."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Sila analisis carta ini dan beri signal penuh God++ Mode."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    result = response.json()

    try:
        return result["choices"][0]["message"]["content"]
    except:
        return "❌ Gagal analisis gambar. Pastikan carta jelas & format betul."
