import requests
import base64
import json
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
from config import OPENAI_API_KEY, BOT_TOKEN, OWNER_ID

# Fungsi analisis dengan GPT-4o
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

# Fungsi bila terima gambar di Telegram
def handle_image(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("❌ Anda tidak dibenarkan.")
        return

    update.message.reply_text("📥 Carta diterima. AI sedang menganalisis...")

    photo_file = update.message.photo[-1].get_file()
    photo_file.download("temp.jpg")

    result = analyze_image_with_gpt("temp.jpg")
    update.message.reply_text(result)

# Fungsi utama
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
