from django.core.cache import cache
from rest_framework.response import Response


class JWTRevocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.COOKIES['jwt_token']
        if jwt_token and cache.get(jwt_token) is not None:
            return Response({"statusCode": 401, "error": "Invalid token"})
        response = self.get_response(request)
        return response
