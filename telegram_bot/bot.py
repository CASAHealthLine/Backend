from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from decouple import config

from telegram_bot.handlers import handle_contact, request_phone

# Khởi tạo bot với token
BOT_TOKEN = config('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào mừng bạn đến với CASA HealthLine! Hãy sử dụng /register để liên kết tài khoản của bạn.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await request_phone(update, context)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Đăng ký các lệnh
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    # Chạy bot
    application.run_polling()

if __name__ == "__main__":
    main()
