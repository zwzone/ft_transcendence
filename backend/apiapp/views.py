from django.conf import settings
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from .serializers import PlayerSerializer, UsernameSerializer, AvatarSerializer
from .models import Player
import jwt
from drf_yasg.utils import swagger_auto_schema
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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
        serializer = PlayerSerializer(user)  # Serialize the Player object
        return Response({
            "status": 200,
            "user": serializer.data  # Return the serialized user data
        })
    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
        })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user_by_username(username):
    try:
        user = Player.objects.get(username=username)
        serializer = PlayerSerializer(user)
        return Response({
            "status": 200,
            "user": serializer.data
        })
    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
        })

@swagger_auto_schema(methods=['put'], request_body=UsernameSerializer)
@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def update_username(request):
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
        username = request.data.get('username')
        if not username:
            return Response({
                "status": 400,
                "message": "Username not provided",
            })
        user.username = username
        user.save()
        serializer = PlayerSerializer(user)
        return Response({
            "status": 200,
            "user": serializer.data
        })
    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": str(e),
        })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_avatar(request):
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
            "avatar": user.Avatar
        })
    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
        })
    except Exception as e:
            return Response({
            "status": 500,
            "message": "what" + str(e),
        })
@swagger_auto_schema(methods=['post'], request_body=AvatarSerializer)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def update_avatar(request):
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

        avatar_file = request.FILES.get('avatar')

        if avatar_file:
            file_path = os.path.join(settings.MEDIA_ROOT, f"avatars/{id}")
            default_storage.save(file_path, ContentFile(avatar_file.read()))
            user.Avatar = file_path
            user.save()

            return Response({
                "status": 200,
                "message": "Avatar uploaded successfully",
            })
        else:
            return Response({
                "status": 400,
                "message": "Avatar file not provided",
            })

    except Player.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User not found",
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": "Error: " + str(e),
        })
