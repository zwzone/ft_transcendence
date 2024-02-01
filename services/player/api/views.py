from django.conf import settings
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlayerSerializer
import jwt
from jwt.exceptions import ExpiredSignatureError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Player, Friendship
from django.db import IntegrityError

class PlayerInfoView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
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
        except ExpiredSignatureError:
            return Response({
                "status": 401,
                "message": "JWT token has expired",
            })
        except Exception as e:
            return Response({
                "status": 500,
                "message": str(e),
            })

    def post(self, request):
        if request.data.get('create') == True:
            try:
                if "jwt_token" not in request.COOKIES:
                    return Response({
                        "message": "JWT token not found in cookies",
                    }, status=status.HTTP_401_UNAUTHORIZED)
                token = request.data.get('token')
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                if Player.objects.filter(email=decoded_token['email']).exists(): 
                    player = Player.objects.get(email=decoded_token['email'])
                    return Response({
                        "message": "User already exists",
                        "id": player.id,
                        "two_factor": player.two_factor
                    }, status=status.HTTP_200_OK)  
                email = decoded_token['email']
                player = request.data.get('player')
                username = player['username']
                first_name = player['first_name']
                last_name = player['last_name']
                avatar = player['avatar']
                player, created = Player.objects.create(email=email, username=username, first_name=first_name,
                                        last_name=last_name, avatar=avatar)
                if created:
                    return Response({
                        "message": "User created successfully",
                        "id": player.id,
                        "two_factor": player.two_factor
                    }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    "message": f"An error occurred while creating the player: {e}",
                }, status=status.HTTP_409_CONFLICT)
            except ExpiredSignatureError:
                return Response({
                    "status": 401,
                    "message": "JWT token has expired",
                }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({
                    "status": 500,
                    "message": str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if "jwt_token" not in request.COOKIES :
                return Response({
                    "message": "JWT token not found in cookies",
                })
            try:
                token = request.COOKIES.get('jwt_token')
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                id = decoded_token['id']
                player_data = request.data.get('player')  
                player = Player.objects.get(id=id)
                if "username" in player_data:
                    player.username = player_data['username']
                if "first_name" in player_data:
                    player.first_name = player_data['first_name']
                if "last_name" in player_data:
                    player.last_name = player_data['last_name']
                if "two_factor" in player_data:
                    if player_data['two_factor'] == True:
                        player.two_factor = True
                    elif player_data['two_factor'] == False:
                        player.two_factor = False
                player.save()
                return Response({
                    "status": 200,
                    "message": "User updated successfully",
                })
            except ExpiredSignatureError:
                return Response({
                    "status": 401,
                    "message": "JWT token has expired",
                })
            except player.DoesNotExist:
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
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.COOKIES.get('jwt_token')
        if not token:
            return Response({
                "status": 401,
                "message": "JWT token not found in cookies",
            })
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            id = decoded_token['id']
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
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        token = request.COOKIES.get('jwt_token')
        if not token:
            return Response({
                "status": 401,
                "message": "JWT token not found in cookies",
            })

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            id = decoded_token['id']
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