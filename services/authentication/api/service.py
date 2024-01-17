from django.db import models
from django.conf import settings
# from apiapp.models import Player
from typing import Dict
import jwt, datetime


def generate_jwt(email: str) -> str:
    payload = {
        'id': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token

def decode_google_id_token(id_token: str) -> Dict[str, str]:
    decoded_token = jwt.decode(id_token, options={"verify_signature": False})
    return decoded_token

def re_encode_jwt(token: str, id: int) -> str:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY)
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidIssuerError
    payload = {
        'id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token
