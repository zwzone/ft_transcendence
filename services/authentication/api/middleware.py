from django.core.cache import cache
from rest_framework.response import Response


def extract_jwt_from_request(request):
    if not 'jwt_token' in request.COOKIES:
        jwt_token = request.COOKIES['jwt_token']
        return jwt_token
    return


class JWTRevocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = extract_jwt_from_request(request)
        if jwt_token:
            if cache.get(jwt_token) is not None:
                return Response({"statusCode": 401, "error": "Invalid token"})
        response = self.get_response(request)
        return response
