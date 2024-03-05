from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from pyotp.totp import TOTP
from base64 import b32encode
from typing import Dict
import datetime
import jwt
from .models import Player


def generate_jwt(id: int, two_factor: bool) -> str:
    payload = {
        'id': id,
        'twofa': two_factor,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token


def decode_google_id_token(id_token: str) -> Dict[str, str]:
    decoded_token = jwt.decode(id_token, options={"verify_signature": False})
    return decoded_token


def get_2fa_qr_code(player_id: int) -> str:
    player_id_encoded = str(player_id).encode("utf-8")
    return TOTP(b32encode(player_id_encoded)).provisioning_uri(name="player", issuer_name="ft_transcendence")


def check_2fa_code(player_id: int, code: int) -> bool:
    player_id_encoded = str(player_id).encode("utf-8")
    return TOTP(b32encode(player_id_encoded)).verify(code)


def jwt_cookie_required(view_func):
    def wrapped_view(request):
        if "jwt_token" not in request.COOKIES:
            return Response({"statusCode": 401, 'error': 'JWT token cookie missing'})
        token = request.COOKIES.get("jwt_token")
        try:
            request.token = token
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if (decoded_token['twofa']):
                return Response({"statusCode": 401, "error": "2FA required"})
            request.decoded_token = decoded_token
            return view_func(request)
        except jwt.ExpiredSignatureError:
            return Response({"statusCode": 401, 'error': 'Token is expired'})
        except jwt.InvalidTokenError:
            return Response({"statusCode": 401, 'error': 'Invalid token'})
        except Exception as e:
            return Response({"statusCode": 500, 'error': str(e)})
    return wrapped_view


def create_player(player_data: Dict[str, str]):
    try:
        email = player_data['email']
        if Player.objects.filter(email=email).exists():
            player = Player.objects.get(email=email)
            return player
        username = player_data['username']
        first_name = player_data['first_name']
        last_name = player_data['last_name']
        avatar = player_data['avatar']
        player = Player.objects.create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
        )
        return player
    except Exception as e:
        return None
