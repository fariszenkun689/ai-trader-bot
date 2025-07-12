from telegram.ext import MessageHandler, Filters
from gpt_vision import analyze_image_with_gpt

def handle_image(update, context):
    if update.effective_user.id != OWNER_ID:
        return
    photo_file = update.message.photo[-1].get_file()
    file_path = "temp.jpg"
    photo_file.download(file_path)
    update.message.reply_text("🧠 Menganalisis carta dengan GPT-4o...")
    result = analyze_image_with_gpt(file_path)
    update.message.reply_text(result)

dp.add_handler(MessageHandler(Filters.photo, handle_image))
from telegram.ext import Updater, CommandHandler
from config import BOT_TOKEN, OWNER_ID
from gold_ai import analyze_market
from utils import format_signal

def start(update, context):
    if update.effective_user.id != OWNER_ID:
        return
    update.message.reply_text("🤖 AI Gold God++ Mode aktif. Hantar /signal untuk analisis.")

def signal(update, context):
    if update.effective_user.id != OWNER_ID:
        return
    result = analyze_market()
    update.message.reply_text(format_signal(result))

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("signal", signal))
updater.start_polling()
updater.idle()
