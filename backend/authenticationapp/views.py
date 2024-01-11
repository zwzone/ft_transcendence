import requests
from os import getenv
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Player


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def intra_auth(request):
    redirect_uri = urlencode({"redirect_uri": request.build_absolute_uri(reverse("callbackView"))})
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={getenv('CLIENT_ID')}&{redirect_uri}&response_type=code"
    return redirect(authorization_url)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def callback_auth(request):
    code = request.GET.get("code")
    error_message = request.GET.get("error")
    if error_message is not None:
        return Response({"statusCode": 401, "error": error_message}, status=status.HTTP_200_OK)
    if code is None:
        return Response({"statusCode": status.HTTP_401_UNAUTHORIZED})
    if request.user.is_authenticated:
        return Response({"statusCode": status.HTTP_200_OK, "Already logged in": error_message})
    data = {
        "grant_type": "authorization_code",
        "client_id": getenv("CLIENT_ID"),
        "client_secret": getenv("CLIENT_SECRET"),
        "code": code,
        "redirect_uri": request.build_absolute_uri(reverse("callbackView")),
    }
    auth_response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
    if "error_description" in auth_response.json():
        return Response({"statusCode": status.HTTP_401_UNAUTHORIZED, "detail": auth_response.get("error_description")},
                        status=status.HTTP_200_OK)
    response = redirect("http://localhost/home")
    response.set_cookie("access_token", auth_response.json()["access_token"])
    response.set_cookie("refresh_token", auth_response.json()["refresh_token"])
    return response
