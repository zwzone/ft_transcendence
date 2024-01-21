from django.core.cache import cache
from django.shortcuts import redirect


class JWTRevocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = self.extract_jwt_from_request(request)
        if jwt_token:
            if self.is_jwt_revoked(jwt_token):
                return redirect("https://localhost/login")
        response = self.get_response(request)
        return response

    def extract_jwt_from_request(self, request):
        # Check if JWT is in the Authorization header
        jwt_header = request.META.get('HTTP_AUTHORIZATION', '')
        # If not found in the header, check if it's in the cookies
        if not jwt_header and 'jwt_token' in request.COOKIES:
            jwt_token = request.COOKIES['jwt_token']
            return jwt_token
        return

    def is_jwt_revoked(self, jwt_token):
        return self.is_token_in_blacklist(jwt_token)

    # the cache is not stored ondisk, and it's limited to the scope of the current Django process
    def is_token_in_blacklist(self, jwt_token):
        return cache.get(jwt_token) is not None
