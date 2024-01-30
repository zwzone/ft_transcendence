import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response


def jwt_cookie_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if "jwt_token" not in request.COOKIES:
            return Response({"statusCode": 401, 'error': 'JWT token cookie missing'})
        token = request.COOKIES.get("jwt_token")
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if cache.get(decoded_token) is not None:
                return Response({"statusCode": 401, "error": "Invalid token"})
            request.decoded_token = decoded_token['id']
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response({"statusCode": 401, 'error': 'Token is expired'})
        except jwt.InvalidTokenError:
            return Response({"statusCode": 401, 'error': 'Invalid token'})
    return wrapped_view
