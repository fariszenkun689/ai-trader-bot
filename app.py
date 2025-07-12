from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
from gpt_vision import analyze_image_with_gpt
from config import BOT_TOKEN, OWNER_ID

def handle_image(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return
    update.message.reply_text("📥 Carta diterima. AI sedang menganalisis...")
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("temp.jpg")
    result = analyze_image_with_gpt("temp.jpg")
    update.message.reply_text(result)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
