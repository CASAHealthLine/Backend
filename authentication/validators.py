import re

def validate_vietnam_phone(phone_number):
    if not phone_number:
        return None
    
    # Chuẩn hóa số điện thoại
    phone_number = re.sub(r"[^\d+]", "", phone_number)

    # Nếu bắt đầu bằng "+84", chuẩn hóa thành "0"
    if phone_number.startswith("+84"):
        phone_number = "0" + phone_number[3:]

    # Kiểm tra độ dài và các đầu số hợp lệ
    if len(phone_number) == 10 and phone_number[:2] in {"03", "05", "07", "08", "09"}:
        return phone_number
    return None