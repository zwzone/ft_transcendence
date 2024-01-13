import requests
from os import getenv
from django.contrib.auth import login
from django.shortcuts import redirect, reverse
from django.utils.http import urlencode
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from .service import GoogleAccessTokens
from .models import Player
# from rest_framework_simplejwt.tokens import RefreshToken


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
        return Response({"statusCode": 401, "detail": auth_response.get("error_description")})
    # TODO: JWT
    return Response({"statusCode": 200, "JWT": ""})

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
    if request.user.is_authenticated:
        return redirect("index")
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
    if not auth_response.ok :
        return Response({"statusCode": 401, "error": "Failed to obtain access token from Google."})
    tokens = auth_response.json()
    google_tokens = GoogleAccessTokens(id_token=tokens["id_token"], access_token=tokens["access_token"])
    if tokens["access_token"] is None:
        return Response({"statusCode": 401, "error": "AccessToken is invalid"})
    id_token_decoded = google_tokens.decode_id_token()
    player_email = id_token_decoded["email"]
    username = id_token_decoded["name"]
    player, created = Player.objects.get_or_create(email=player_email, username=username)
    if created:
        print(player_email)
    if player is None:
        return Response({"statusCode": 401, "error": "can't create player"})
    login(request, player)

    result = {
        "id_token_decoded": id_token_decoded,
        "player_email": player_email,
    }
    return Response(result)
