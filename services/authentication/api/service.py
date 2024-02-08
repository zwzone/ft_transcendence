from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from pyotp.totp import TOTP
from base64 import b32encode
from typing import Dict
import datetime
import jwt


def generate_jwt(id: int, authority: bool) -> str:
    payload = {
        'id': id,
        'authority': authority,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        'iat': datetime.datetime.utcnow(),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token


def decode_google_id_token(id_token: str) -> Dict[str, str]:
    decoded_token = jwt.decode(id_token, options={"verify_signature": False})
    return decoded_token


def check_2fa_code(player_id: int, code: int) -> bool:
    player_id = str(player_id)
    print("CHECK_2FA_CODE -> code:", code)
    print("-----------------------")
    totp = TOTP(b32encode(player_id.encode("utf-8")))
    print("+++++++++++++++++++++++")
    check = totp.verify(code)
    print("***********************")
    return check


def jwt_cookie_required(view_func):
    def wrapped_view(request):
        if "jwt_token" not in request.COOKIES:
            return Response({"statusCode": 401, 'error': 'JWT token cookie missing'})
        token = request.COOKIES.get("jwt_token")
        if cache.get(token) is not None:
            return Response({"statusCode": 401, "error": "Invalid token"})
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.decoded_token = decoded_token
            return view_func(request)
        except jwt.ExpiredSignatureError:
            return Response({"statusCode": 401, 'error': 'Token is expired'})
        except jwt.InvalidTokenError:
            return Response({"statusCode": 401, 'error': 'Invalid token'})
        except Exception as e:
            return Response({"statusCode": 500, 'error': str(e)})
    return wrapped_view
