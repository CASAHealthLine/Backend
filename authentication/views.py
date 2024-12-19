import requests
from itsdangerous import URLSafeTimedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from decouple import config

from authentication.validators import validate_vietnam_phone
from .models import OTP, ContactLink
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from tenacity import retry, wait_fixed, stop_after_attempt
from django.utils.timezone import now

API_SECRET_TOKEN=config('API_SECRET_TOKEN')

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        otp_code = request.data.get('otp')
        phone_number = request.data.get('phone') or request.COOKIES.get('otp_phone')

        if not otp_code or not phone_number:
            return Response({'error': 'Missing phone_number or otp'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validate_vietnam_phone(phone_number):
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
        
        success, message = verify_otp(phone_number, otp_code)
        
        secret_token = generate_otp_token(API_SECRET_TOKEN, otp_code, phone_number)
        
        if success:
            response = Response({'message': message}, status=status.HTTP_200_OK)
            response.set_cookie('otp_token', secret_token, max_age=300, samesite='Lax', httponly=True)
            return response
        else:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
            
class LinkPhoneView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        auth_header = request.headers.get("X-Api-Token")

        if not auth_header or auth_header != API_SECRET_TOKEN:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        user_agent = request.headers.get("User-Agent")
        
        phone_number = request.data.get("phone")
        tele_id = request.data.get("tele_id")

        if not phone_number or not tele_id:
            return Response({"error": "Missing phone_number or tele_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validate_vietnam_phone(phone_number):
            return Response({"error": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)

        contact, created = ContactLink.objects.update_or_create(
            phone_number=phone_number,
            defaults={"tele_id": tele_id},
        )

        if created:
            return Response({"message": "Phone number linked successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Phone number already linked."}, status=status.HTTP_200_OK)
        
class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        phone_number = request.data.get("phone") or request.COOKIES.get("otp_phone")
        if not phone_number:
            return Response({"error": "Missing phone_number"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validate_vietnam_phone(phone_number):
            return Response({"error": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)
        
        success, message = request_and_send_otp(phone_number)
        
        if success:
            response = Response({"message": message}, status=status.HTTP_200_OK)
            response.set_cookie("otp_phone", phone_number, max_age=300, samesite="Lax", httponly=True)
            return response
        else:
            return Response({"error": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def request_and_send_otp(phone_number):
    contact = ContactLink.objects.filter(phone_number=phone_number).first()
    if not contact:
        return False, "Phone number not linked"
    
    otp_code = OTP.generate_otp(phone_number)

    if contact.tele_id:
        try:
            send_otp_to_telegram(contact.tele_id, otp_code)
        except Exception as e:
            print(f"Error sending OTP to Telegram: {e}")
            return False, "Error sending OTP to Telegram"
    return True, "OTP sent successfully"

def verify_otp(phone_number, otp_code):
    try:
        otp_record = OTP.objects.get(phone_number=phone_number)
        if otp_record.otp == otp_code and otp_record.expires_at > now():
            otp_record.delete()
            return True, "OTP verified successfully"
        else:
            return False, "Invalid or expired OTP"
    except OTP.DoesNotExist:
        return False, "OTP record not found"
    
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def send_otp_to_telegram(tele_id, otp_code):
    BOT_TOKEN = config('BOT_TOKEN')
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": tele_id, "text": f"Mã OTP của bạn là: {otp_code}"}
    requests.post(url, data=payload, timeout=5)
        
def save_contact(phone_number, tele_id=None, email=None):
    contact, created = ContactLink.objects.update_or_create(
        phone_number=phone_number,
        defaults={
            'tele_id': tele_id,
            'email': email,
        }
    )
    if created:
        print(f"New contact created: {phone_number}")
    else:
        print(f"Contact updated: {phone_number}")
        
def generate_otp_token(secret_key, code, number):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps({'code': code, 'number': number})

def verify_otp_token(secret_key, token, code, number):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        data = serializer.loads(token, max_age=300)
        return data['code'] == code and data['number'] == number
    except:
        return False