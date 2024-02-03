from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlayerSerializer
from .models import Player, Friendship
from .decorators import jwt_cookie_required
import urllib.parse
import os


class PlayerInfo(APIView):

    @method_decorator(jwt_cookie_required)
    def get(self, request):
        try:
            user = Player.objects.get(id=request.decoded_token['id'])
            serializer = PlayerSerializer(user)
            return Response({
                "status": 200,
                "player": serializer.data
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

    @method_decorator(jwt_cookie_required)
    def post(self, request):
        if "email" in request.decoded_token:
            email = request.decoded_token['email']
            if Player.objects.filter(email=email).exists():
                player = Player.objects.get(email=email)
                return Response({
                    "message": "User already exists",
                    "id": player.id,
                    "two_factor": player.two_factor
                }, status=status.HTTP_200_OK)
            player = request.data.get('player')
            username = player['username']
            first_name = player['first_name']
            last_name = player['last_name']
            avatar = player['avatar']
            try:
                player = Player.objects.create(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    avatar=avatar
                )
                return Response({
                    "message": "User created successfully",
                    "id": player.id,
                    "two_factor": player.two_factor
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    "message": f"An error occurred while creating the player: {e}",
                }, status=status.HTTP_409_CONFLICT)
            except Exception as e:
                return Response({
                    "message": str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif "id" in request.decoded_token:
            try:
                id = request.decoded_token['id']
                player_data = request.data.get('player')  
                player = Player.objects.get(id=id)
                if "username" in player_data:
                    player.username = player_data['username']
                if "first_name" in player_data:
                    player.first_name = player_data['first_name']
                if "last_name" in player_data:
                    player.last_name = player_data['last_name']
                if "two_factor" in player_data:
                    player.two_factor = player_data['two_factor']
                player.save()
                return Response({
                    "status": 200,
                    "message": "User updated successfully",
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


class PlayerAvatarUpload(APIView):

    @method_decorator(jwt_cookie_required)
    def post(self, request):
        try:
            id = request.decoded_token['id']
            file = request.FILES['avatar']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            default_storage.save(file_path, ContentFile(file.read()))
            file_url = urllib.parse.urljoin(settings.PUBLIC_PLAYER_URL, os.path.join(settings.MEDIA_URL, file.name))
            player = Player.objects.get(id=id)
            player.avatar = file_url
            player.save()
            return Response({
                "status": 200,
                "message": "Avatar updated successfully",
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


class PlayerAddFriend(APIView):

    @method_decorator(jwt_cookie_required)
    def post(self, request):
        id = request.decoded_token['id']
        try:
            sender_username = Player.objects.get(id=id)
            receiver_username = request.data.get('receiver_username')
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
        try:
            sender = Player.objects.get(username=sender_username)
            receiver = Player.objects.get(username=receiver_username)
            friendship = Friendship.objects.create(sender=sender, receiver=receiver)
            friendship.pending = True
            friendship.save()
            return Response({
                "status": 200,
                "message": "Friend request sent successfully"
            })
        except Player.DoesNotExist:
            return Response({
            "status": 404,
            "message": "Player not found"
        })


class AcceptFriendRequest(APIView):

    @method_decorator(jwt_cookie_required)
    def post(self, request):
        id = request.decoded_token['id']
        try:
            receiver_username = Player.objects.get(id=id)
            sender_username = request.data.get('sender_username')
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
        try:
            sender = Player.objects.get(username=sender_username)
            receiver = Player.objects.get(username=receiver_username)
            friendship = Friendship.objects.get(sender=sender, receiver=receiver)
            friendship.accepted = True
            friendship.pending = False
            friendship.save()
            return Response({
                "status": 200,
                "message": "Friend request accepted successfully"
            })
        except Player.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Player not found"
            })
        except Friendship.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Friendship not found"
            })
