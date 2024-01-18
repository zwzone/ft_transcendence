from django.http import HttpResponseForbidden
from django.core.cache import cache
import jwt
from services.authentication.api import settings


class JWTRevocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = self.extract_jwt_from_request(request)

        if jwt_token:
            if self.is_jwt_revoked(jwt_token):
                return HttpResponseForbidden('JWT revoked. Please log in again.')
            user_info = self.extract_user_info_from_jwt(jwt_token)
            request.user_info = user_info
        response = self.get_response(request)
        return response

    def extract_jwt_from_request(self, request):
        jwt_header = request.META.get('HTTP_AUTHORIZATION', '')
        jwt_token = jwt_header.split(' ')[1] if 'HTTP_AUTHORIZATION' in request.META else None
        return jwt_token

    def is_jwt_revoked(self, jwt_token):
        return self.is_token_in_blacklist(jwt_token)

    def is_token_in_blacklist(self, jwt_token):
        return cache.get(jwt_token) is not None

    def extract_user_info_from_jwt(self, jwt_token):
        decoded_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_info = decoded_token.get('id', {})
        return user_info
