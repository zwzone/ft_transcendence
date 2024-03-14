import re
import jwt
from django.db import close_old_connections
from channels.auth import AuthMiddlewareStack
from .settings import SECRET_KEY

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
                scope['payload'] = self.decode_token(token_key)
                if scope['payload'] is not None:
                    return await self.inner(scope, receive, send)
        return

    def decode_token(self, token_key):
        try:
            payload = jwt.decode(token_key, SECRET_KEY, algorithms=['HS256'])
            if (payload['twofa']):
                return None
            return payload
        except jwt.InvalidTokenError:
            return None

MyAuthMiddlewareStack = lambda inner: TokenMiddleware(AuthMiddlewareStack(inner))
