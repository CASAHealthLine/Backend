import httpx
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from decouple import config

from authentication.validators import validate_vietnam_phone

API_URL = "http://localhost:8000/api/auth/link-phone/"
API_SECRET_TOKEN=config('API_SECRET_TOKEN')

# Gửi số điện thoại và chat_id tới API Django
async def send_phone_to_django(phone_number, chat_id):
    async with httpx.AsyncClient() as client:
        data = {
            "phone": phone_number,
            "tele_id": chat_id,
        }
        headers = {
            "X-Api-Token": API_SECRET_TOKEN,
        }
        response = await client.post(API_URL, data=data, headers=headers)
        return response.status_code, response.json()


# Hàm yêu cầu chia sẻ số điện thoại
async def request_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Chia sẻ số điện thoại", request_contact=True)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    # Sử dụng await trước reply_text
    await update.message.reply_text(
        "Vui lòng chia sẻ số điện thoại của bạn để liên kết tài khoản và nhận thông báo từ CASA HealthLine.",
        reply_markup=reply_markup,
    )


# Hàm xử lý khi người dùng chia sẻ số điện thoại
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        phone_number = contact.phone_number
        chat_id = update.message.chat_id
        
        # Kiểm tra số điện thoại
        phone_number = validate_vietnam_phone(phone_number)
        if not phone_number:
            await update.message.reply_text("Xin lỗi, hiện tại chúng tôi chỉ hỗ trợ số điện thoại Việt Nam.")

        # Gửi dữ liệu tới API Django
        status, response = await send_phone_to_django(phone_number, chat_id)
        if status == 200:
            await update.message.reply_text("Số điện thoại của bạn đã được liên kết thành công!")
        else:
            await update.message.reply_text("Đã xảy ra lỗi khi liên kết số điện thoại. Vui lòng thử lại sau.")
