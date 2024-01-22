import requests
from os import getenv
from django.shortcuts import redirect, reverse
from django.utils.http import urlencode
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from .service import decode_google_id_token, generate_jwt, re_encode_jwt
from django.conf import settings
import jwt
from django.core.cache import cache


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def intra_auth(request):
    redirect_uri = urlencode({"redirect_uri": request.build_absolute_uri(reverse("intracallbackView"))})
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={getenv('INTRA_CLIENT_ID')}&{redirect_uri}&response_type=code"
    return redirect(authorization_url)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
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
        "redirect_uri": request.build_absolute_uri(reverse("intracallbackView")),
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
    jwt_token = generate_jwt(user_data["email"])
    data = {
        "token": jwt_token,
        "player": {
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "username": user_data["login"],
            "avatar": user_data["image"]["link"],
        }
    }
    player_data = requests.post(f'{settings.PLAYER_URL}/', json=data)
    if not player_data.ok:
        return redirect("https://localhost/login")
    player_id = player_data.json()['id']
    jwt_token = re_encode_jwt(player_id)
    response = redirect("https://localhost/home")
    response.set_cookie("jwt_token", value=jwt_token, httponly=True, secure=True)
    return response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def google_auth(request):
    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]
    params = {
        "response_type": "code",
        "client_id": getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": request.build_absolute_uri(reverse("googlecallbackView")),
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
@authentication_classes([])
@permission_classes([])
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
        "redirect_uri": request.build_absolute_uri(reverse("googlecallbackView")),
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
    jwt_token = generate_jwt(id_token_decoded['email'])
    data = {
        "token": jwt_token,
        "player": {
            "email": id_token_decoded['email'],
            "first_name": id_token_decoded['given_name'],
            "last_name": id_token_decoded['family_name'],
            "username": id_token_decoded['name'],
            "avatar": id_token_decoded['picture'],
        }
    }
    player_data = requests.post(f'{settings.PLAYER_URL}/', json=data)
    if not player_data.ok:
        return redirect("https://localhost/login")
    player_id = player_data.json()['id']
    jwt_token = re_encode_jwt(player_id)
    response = redirect("https://localhost/home")
    response.set_cookie("jwt_token", value=jwt_token, httponly=True, secure=True)
    return response

@api_view(["GET"])
def is_logged_in_auth(request):
    jwt_token = request.COOKIES.get("jwt_token")
    if jwt_token is None:
        return Response({"statusCode": 404, "error": "Invalid token"})
    try:
        jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        return Response({"statusCode": 200, "message": "Token is valid"})
    except jwt.ExpiredSignatureError:
        return Response({"statusCode": 404, "error": "Token has expired"})
    except jwt.InvalidTokenError:
        return Response({"statusCode": 404, "error": "Invalid token"})

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def logout_user(request):
    jwt_token = request.COOKIES.get("jwt_token")
    if jwt_token is not None:
        cache.set(jwt_token, True, timeout=None)
        response = redirect("https://localhost/login")
        response.delete_cookie('jwt_token')
        return response
    else:
        return Response({"statusCode": 400, "detail": "No valid access token found"})
