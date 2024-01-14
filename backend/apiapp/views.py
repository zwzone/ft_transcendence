from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .serializers import UserSerializer
from .models import Player


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def player_api(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return Response({
            "status": 401,
            "message": "JWT token not found in cookies",
        })
    try:
        decoded_token = AccessToken(token)
        user_id = decoded_token['user_id']
        user = Player.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response({
            "status": 200,
            "player": serializer.data
        })
    except InvalidToken as e:
        return Response({
            "status": 401,
            "message": str(e),
        })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user_by_username(request, username):
    try:
        user = Player.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response({
            "status": 200,
            "user": serializer.data
        })
    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
        })
