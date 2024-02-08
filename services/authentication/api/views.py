from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import urlencode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .service import decode_google_id_token, generate_jwt, check_2fa_code, jwt_cookie_required, get_2fa_qr_code
from os import getenv
from qr_code.qrcode.maker import make_qr_code_image
from qr_code.qrcode.utils import QRCodeOptions
import requests
import jwt


@api_view(['GET'])
def intra_auth(request):
    redirect_uri = urlencode({"redirect_uri": f"{settings.PUBLIC_AUTHENTICATION_URL}intra/callback/"})
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={getenv('INTRA_CLIENT_ID')}&{redirect_uri}&response_type=code"
    return redirect(authorization_url)


@api_view(['GET'])
def intra_callback_auth(request):
    code = request.GET.get("code")
    error_message = request.GET.get("error")
    if error_message is not None:
        return Response({"statusCode": 401, "error": error_message})
    if code is None:
        return Response({"statusCode": 401, "error": "code is required"})
    if request.user.is_authenticated:
        return Response({"statusCode": 200, "message": "Already logged in"})
    data = {
        "grant_type": "authorization_code",
        "client_id": getenv("INTRA_CLIENT_ID"),
        "client_secret": getenv("INTRA_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": f"{settings.PUBLIC_AUTHENTICATION_URL}intra/callback/",
    }
    auth_response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
    if not auth_response.ok:
        return Response({"statusCode": 401})
    access_token = auth_response.json()["access_token"]
    user_response = requests.get(
        "https://api.intra.42.fr/v2/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if not user_response.ok:
        return Response({"statusCode": 401, "detail": "No access token in the token response"})
    user_data = user_response.json();
    jwt_token = generate_jwt(None, True)
    data = {
        "player": {
            "email": user_data["email"],
            "username": user_data["login"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "avatar": user_data["image"]["link"],
        }
    }
    player_data = requests.post(f'{settings.PRIVATE_PLAYER_URL}', json=data, cookies={"jwt_token": jwt_token})
    if not player_data.ok:
        return redirect(f"https://{settings.FT_TRANSCENDENCE_HOST}/login/")
    if player_data.json()['two_factor']:
        return Response({"statusCode": 200, "id": player_data.json()['id'], 'message': 'Enable two-factor'})
    player_id = player_data.json()['id']
    jwt_token = generate_jwt(player_id, False)
    response = redirect(f"https://{settings.FT_TRANSCENDENCE_HOST}/home/")
    response.set_cookie("jwt_token", value=jwt_token, httponly=True, secure=True)
    return response


@api_view(["GET"])
def google_auth(request):
    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]
    params = {
        "response_type": "code",
        "client_id": getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": f'{settings.PUBLIC_AUTHENTICATION_URL}google/callback/',
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "select_account",
    }
    query_params = urlencode(params)
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    google_authorization_url = f"{GOOGLE_AUTH_URL}?{query_params}"
    return redirect(google_authorization_url)


@api_view(["GET"])
def google_callback_auth(request):
    code = request.GET.get("code")
    error = request.GET.get("error")
    if error is not None:
        return Response({"statusCode": 401, "error": error})
    if code is None:
        return Response({"statusCode": 401, "error": "User Not Autorized"})
    data = {
        "code": code,
        "client_id": getenv("GOOGLE_CLIENT_ID"),
        "client_secret": getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": f'{settings.PUBLIC_AUTHENTICATION_URL}google/callback/',
        "grant_type": "authorization_code",
    }
    auth_response = requests.post("https://oauth2.googleapis.com/token", data=data)
    if not auth_response.ok:
        return Response({"statusCode": 401, "error": "Failed to obtain access token from Google."})
    tokens = auth_response.json()
    if tokens["access_token"] is None:
        return Response({"statusCode": 401, "error": "AccessToken is invalid"})
    id_token = tokens["id_token"]
    id_token_decoded = decode_google_id_token(id_token)
    jwt_token = generate_jwt(None, True)
    data = {
        "player": {
            "email": id_token_decoded['email'],
            "username": id_token_decoded['name'],
            "first_name": id_token_decoded['given_name'],
            "last_name": id_token_decoded['family_name'],
            "avatar": id_token_decoded['picture'],
        }
    }
    player_data = requests.post(f'{settings.PRIVATE_PLAYER_URL}', json=data, cookies={"jwt_token": jwt_token})
    if not player_data.ok:
        return redirect(f"https://{settings.FT_TRANSCENDENCE_HOST}/login/")
    if player_data.json()['two_factor']:
        return Response({"statusCode": 200, "id": player_data.json()['id'], 'message': 'Enable two-factor'})
    player_id = player_data.json()['id']
    jwt_token = generate_jwt(player_id, False)
    response = redirect(f"https://{settings.FT_TRANSCENDENCE_HOST}/home/")
    response.set_cookie("jwt_token", value=jwt_token, httponly=True, secure=True)
    return response


@api_view(["GET"])
@jwt_cookie_required
def is_logged_in_auth(request):
    return Response({"statusCode": 200, "message": "Token is valid"})


@api_view(["GET"])
@jwt_cookie_required
def logout_user(request):
    if request.decoded_token is not None:
        cache.set(request.decoded_token, True, timeout=None)
        response = redirect(f"https://{settings.FT_TRANSCENDENCE_HOST}/login/")
        response.delete_cookie("jwt_token")
        return response
    else:
        return Response({"statusCode": 400, "detail": "No valid access token found"})


@api_view(["POST"])
@jwt_cookie_required
def verify_two_factor(request):
    code = request.data.get("code")
    player_id = request.data.get("id")
    if player_id is None:
        player_id = request.decoded_token['id']
        if not check_2fa_code(player_id, code):
            return Response({"statusCode": 401, "message": "Incorrect 2FA code."})
        return Response({"statusCode": 200, "message": "Successfully verified"})
    else:
        if not check_2fa_code(player_id, code):
            return Response({"statusCode": 401, "message": "Incorrect 2FA code."})
        jwt_token = generate_jwt(player_id, False)
        response = redirect(f"https://{settings.FT_TRANSCENDENCE_HOST}/home/")
        response.set_cookie("jwt_token", value=jwt_token, httponly=True, secure=True)
        requests.post(f'{settings.PRIVATE_PLAYER_URL}2fa/', json={"2fa": True})
        return Response({"statusCode": 200, "message": "Successfully verified"})


@api_view(["GET"])
@jwt_cookie_required
def enable_two_factor(request):
    token = request.COOKIES.get("jwt_token")
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    player_id = decoded_token['id']
    qr_code = get_2fa_qr_code(player_id)
    image = make_qr_code_image(qr_code, QRCodeOptions(), True);
    return HttpResponse(image, content_type='image/svg+xml')
