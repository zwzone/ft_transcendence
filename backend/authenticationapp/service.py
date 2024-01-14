from django.db import models
from django.conf import settings
from apiapp.models import Player
from typing import Dict
import jwt, datetime


def generate_jwt(player):
    payload ={
        'id': player.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    print("iat =>", payload['iat'])
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token

def decode_jwt(jwt_token):
    if not jwt_token:
        raise jwt.InvalidIssuerError
    try:
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidIssuerError
    player = Player.objects.get(pk=payload['id'])
    # serializer = PlayerSerializer(user)
    return player


class GoogleAccessTokens(models.Model):
    id_token = models.TextField()
    access_token = models.TextField()
    def decode_id_token(self) -> Dict[str, str]:
        id_token = self.id_token
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        return decoded_token
