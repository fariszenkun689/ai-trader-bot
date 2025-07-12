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
