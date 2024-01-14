from django.conf import settings
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Player
import jwt

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
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        id = decoded_token['id']
        user = Player.objects.get(id=id)
        return Response({
            "status": 200,
            "user": {
                "id": user.id,
                "username": user.username,
                # Add other user attributes here
            }
        })
    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
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
