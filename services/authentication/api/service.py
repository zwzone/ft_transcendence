from typing import Dict
import jwt, datetime
from django.conf import settings
from .guard import totp, hotp_secret


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
    secret_key = settings.SECRET_KEY
    secret_2fa = hotp_secret(player_id, secret_key)
    return totp(secret_2fa) != code
