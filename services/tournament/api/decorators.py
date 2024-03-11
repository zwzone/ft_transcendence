from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
import jwt


def jwt_cookie_required(view_func):
    def wrapped_view(request):
        if "jwt_token" not in request.COOKIES:
            return Response({"statusCode": 401, 'error': 'JWT token cookie missing'})
        token = request.COOKIES.get("jwt_token")
        if cache.get(token) is not None:
            return Response({"statusCode": 401, "error": "Invalid token"})
        try:
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
