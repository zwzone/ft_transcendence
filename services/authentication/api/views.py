import requests
from os import getenv
from django.shortcuts import redirect, reverse
from django.utils.http import urlencode
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from .service import GoogleAccessTokens, generate_jwt, re_encode_jwt
from django.conf import settings


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
    # TODO: should be understood
    if request.user.is_authenticated:
        return redirect("http://localhost/home")
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
    access_token = auth_response.json()["access_token"]
    user_response = requests.get(
        "https://api.intra.42.fr/v2/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if not user_response.ok:
        return Response({"statusCode": 401, "detail": "No access token in the token response"})
    api_response, error = requests.post(f'{settings.BASE_URL}/app2/view_in_app2/', user_response)
    # email = user_response.json()["email"]
    # username = user_response.json()["displayname"]
    # player, created = Player.objects.get_or_create(email=email, username=username)
    # if player is None:
    #     return Response({"statusCode": 401, "error": "can't create or get player"})
    jwt_token = generate_jwt(api_response.json(["id"]))
    # TODO :: hit the  creat a  new player end point in the api app
    response = redirect(f'{settings.BASE_URL}/home/')
    response.set_cookie("jwt_token", value=jwt_token, httponly=True)
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


# TODO: This should be tested with Postman because of the first if condition
@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def google_callback_auth(request):
    # TODO: should be understood
    if request.user.is_authenticated:
        return redirect("http://localhost/home")
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
    google_tokens = GoogleAccessTokens(id_token=tokens["id_token"], access_token=tokens["access_token"])
    id_token_decoded = google_tokens.decode_id_token()
    if error is not None:
        return Response({"statusCode": 401, "error": "AccessToken is invalid"})
    # TODO: change this to Our id  system
    jwt_token = generate_jwt(id_token_decoded.json(['email']))
    data = {
        "token": jwt_token,
        "player": {
            "email": id_token_decoded.json(['email']),
            "first_name": id_token_decoded.json(["given_name"]),
            "last_name": id_token_decoded.json(["family_name"]),
            "username": id_token_decoded.json(["name"]),
            "avatar": id_token_decoded.json(["picture"]),
        }
    }
    player_data = requests.post(f'{settings.PLAYER_URL}/player/create', data=data)
    if not player_data.ok:
        return redirect("http://localhost/login")
    jwt_token = re_encode_jwt(player_data.json(['id']))
    response = redirect("http://localhost/home")
    response.set_cookie("jwt_token", value=jwt_token, httpsonly=True)
    return response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def is_logged_in_auth(request):
    access_token = request.COOKIES["access_token"]
    refresh_token = request.COOKIES["refresh_token"]
    if access_token is None or refresh_token is None:
        return Response({"statusCode": 401, "error": "invalid"})
