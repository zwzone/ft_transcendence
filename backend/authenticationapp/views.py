import requests
from os import getenv
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Player


class PlayerSerializer(serializers.Serializer):
    username = serializers.CharField()
    display_name = serializers.CharField()


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class IntraRedirectAPIView(PublicApi):
    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse("authAPI"))
        authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={getenv('CLIENT_ID')}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(authorization_url)


class IntraAuthAPIView(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse("authAPI"))
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        code = validated_data.get("code")
        error_message = validated_data.get("error")
        if error_message is not None:
            return Response(
                dict(statusCode=401, error=error_message), status=status.HTTP_200_OK
            )
        if code is None:
            return Response({"statusCode": status.HTTP_401_UNAUTHORIZED})
        if request.user.is_authenticated:
            return Response(
                {"statusCode": status.HTTP_200_OK, "Already logged in": error_message}
            )
        code: str = request.GET.get("code")
        if code:
            return Response(
                {"statusCode": 200, "Already logged in": error_message},
                status=status.HTTP_200_OK,
            )
        data = {
            "grant_type": "authorization_code",
            "client_id": getenv("CLIENT_ID"),
            "client_secret": getenv("CLIENT_SECRET"),
            "code": code,
            "redirect_uri": redirect_uri,
        }
        auth_response = requests.post(
            "https://api.intra.42.fr/oauth/token",
            data=data,
        )
        if "error_description" in auth_response.json():
            return Response(
                {
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                    "detail": auth_response.json().get("error_description"),
                },
                status=status.HTTP_200_OK,
            )
        access_token = auth_response.json()["access_token"]
        user_response = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if not user_response or user_response.status_code != 200:
            return Response(
                {
                    "statusCode": status.HTTP_403_FORBIDDEN,
                    "detail": "No access token in the token response",
                }
            )
        username = user_response.json()["login"]
        display_name = user_response.json()["displayname"]
        email = user_response.json()["email"]
        try:
            # print(Player.objects.get(username=username))
            # user = Player.objects.get(username=username)
            user = get_user_model().objects.get(username=username)
            return Response({"statusCode": 200}, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            user = Player.objects.create_user(
                username=username, display_name=display_name, email=email
            )
            login(request, user)
            return Response({"statusCode": 200}, status=status.HTTP_200_OK)
