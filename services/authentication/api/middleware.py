from django.core.cache import cache
from rest_framework.response import Response
import re
import jwt
from django.db import close_old_connections
from channels.auth import AuthMiddlewareStack
from .settings import SECRET_KEY
from .models import Player
from channels.db import database_sync_to_async


class JWTRevocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.COOKIES.get("jwt_token")
        if jwt_token and cache.get(jwt_token) is not None:
            return Response({"statusCode": 401, "error": "Token is revoked"})
        response = self.get_response(request)
        return response

@database_sync_to_async
def get_player_by_id(id):
    return Player.objects.get(id=id)

class TokenMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope["headers"])
        if b"cookie" in headers:
            cookies = headers[b"cookie"].decode()
            match = re.search("jwt_token=(.*)", cookies)
            if match is not None:
                token_key = match.group(1)
                await self.decode_token(token_key, scope)
                return await self.inner(scope, receive, send)
        scope['status'] = "Invalid"
        return await self.inner(scope, receive, send)

    async def decode_token(self, token_key, scope):
        try:
            payload = jwt.decode(token_key, SECRET_KEY, algorithms=['HS256'])
            if (payload['twofa']):
                scope['status'] = "Twofa"
            scope['player'] = await get_player_by_id(payload['id'])
            scope['status'] = "Valid"
        except Player.DoesNotExist:
            scope['status'] = "Invalid"
        except jwt.InvalidTokenError:
            scope['status'] = "Invalid"


MyAuthMiddlewareStack = lambda inner: TokenMiddleware(AuthMiddlewareStack(inner))
