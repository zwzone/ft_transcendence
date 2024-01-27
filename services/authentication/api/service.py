from typing import Dict
import jwt, datetime
from django.conf import settings
import base64, hashlib
from rest_framework.response import Response


def generate_jwt(email: str) -> str:
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        'iat': datetime.datetime.utcnow(),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token


def decode_google_id_token(id_token: str) -> Dict[str, str]:
    decoded_token = jwt.decode(id_token, options={"verify_signature": False})
    return decoded_token


def re_encode_jwt(id: int) -> str:
    payload = {
        'id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token


def two_factor_auth(player_data: Dict[str, str]):
    hashed_secret = hashlib.sha512(player_data['id'] + settings.SECRET_KEY.encode("utf-8")).digest()
    encoded_secret = base64.b32encode(hashed_secret)
    return Response({
        "status": "pending",
        "message": "Please submit your 2FA code.",
        "key": encoded_secret.decode('utf-8')
    })
