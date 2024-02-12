from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from rest_framework import status
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
            player = Player.objects.get(id=request.decoded_token['id'])
            serializer = PlayerSerializer(player)
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
        if request.decoded_token['authority']:
            player_data = request.data.get('player')
            email = player_data['email']
            if Player.objects.filter(email=email).exists():
                player = Player.objects.get(email=email)
                return Response({
                    "message": "User already exists",
                    "id": player.id,
                    "two_factor": player.two_factor
                }, status=status.HTTP_200_OK)
            username = player_data['username']
            first_name = player_data['first_name']
            last_name = player_data['last_name']
            avatar = player_data['avatar']
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
            except IntegrityError as e:
                return Response({
                    "message": f"An error occurred while creating the player: {e}",
                }, status=status.HTTP_409_CONFLICT)
            except Exception as e:
                return Response({
                    "message": str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                changed = False
                id = request.decoded_token['id']
                player_data = request.data.get('player')
                player = Player.objects.get(id=id)
                if "username" in player_data:
                    if not player_data['username'].isalnum() \
                        and '_' not in player_data['username'] \
                        or len(player_data['username']) > 8 \
                        or len(player_data['username']) < 3:
                        return Response({
                            "status": 400,
                            "message": "Username invalid",
                        })
                    player.username = ' '.join(player_data['username'].split())
                    changed = True
                if "first_name" in player_data:
                    first_name = ' '.join(player_data['first_name'].split())
                    if not first_name.isalpha() or \
                        len(first_name) > 20 or \
                        len(first_name) < 2:
                        return Response({
                            "status": 400,
                            "message": "First name is invalid",
                        })
                    player.first_name = first_name
                    changed = True
                if "last_name" in player_data:
                    last_name = ' '.join(player_data['last_name'].split())
                    if not last_name.isalpha() \
                        or len(last_name) > 20 \
                        or len(last_name) < 2:
                        return Response({
                            "status": 400,
                            "message": "Last name invalid",
                        })
                    player.last_name = ' '.join(player_data['last_name'].split())
                    changed = True
                if "two_factor" in player_data and (request.decoded_token['authority'] is True or player_data['two_factor'] is False):
                    player.two_factor = player_data['two_factor']
                    changed = True
                player.save()
                message = "User updated successfully" if changed else "No changes detected"
                return Response({
                    "status": 200,
                    "message": message,
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


class PlayerFriendship(APIView):

        @method_decorator(jwt_cookie_required)
        def get(self, request):
            id = request.decoded_token['id']
            try:
                get_type = request.query_params.get('target')
                if get_type == 'invitations':
                    friendships = Friendship.objects.filter(receiver=id, status='PN')
                    friendship_data = []
                    for friendship in friendships:
                        friend = friendship.sender
                        friend_data = {
                            "username": friend.username,
                            "avatar": friend.avatar
                        }
                        friendship_data.append(friend_data)
                    return Response({
                        "status": 200,
                        "friendships": friendship_data
                    })
                elif get_type == 'friends':
                    friendships = Friendship.objects.filter(sender=id, status='AC')
                    friendship_data = []
                    for friendship in friendships:
                        friend = friendship.receiver
                        friend_data = {
                            "username": friend.username,
                            "avatar": friend.avatar
                        }
                        friendship_data.append(friend_data)
                    return Response({
                        "status": 200,
                        "friendships": friendship_data
                    })
                elif get_type == 'requests':
                    friendships = Friendship.objects.filter(sender=id, status='PN')
                    friendship_data = []
                    for friendship in friendships:
                        friend = friendship.receiver
                        friend_data = {
                            "username": friend.username,
                            "avatar": friend.avatar
                        }
                        friendship_data.append(friend_data)
                    return Response({
                        "status": 200,
                        "friendships": friendship_data
                    })
                else:
                    return Response({
                        "status": 400,
                        "message": "Invalid request",
                    })
            except Exception as e:
                return Response({
                    "status": 500,
                    "message": str(e),
                })

        @method_decorator(jwt_cookie_required)
        def post(self, request):
            id = request.decoded_token['id']
            try:
                sender = Player.objects.get(id=id)
                receiver_id = request.data.get('target_id')
                if receiver_id == id:
                    return Response({
                        "status": 400,
                        "message": "You can't send a friend request to yourself",
                    })
                receiver = Player.objects.get(id=receiver_id)
                if Player.objects.filter(id=receiver_id).exists():
                    if Friendship.objects.filter(sender=sender, receiver=receiver).exists():
                        friendship = Friendship.objects.get(sender=sender, receiver=receiver)
                        friendship.status = 'AC'
                        friendship.save()
                        return Response({
                                "status": 200,
                                "message": "Friend request accepted successfully"
                            })
                    friendship = Friendship.objects.create(sender=sender, receiver=receiver, status='PN')
                    friendship.save()
                    return Response({
                        "status": 200,
                        "message": "Friend request sent successfully"
                    })
            except Player.DoesNotExist:
                return Response({
                    "status": 404,
                    "message": "User not found",
                })
            except Friendship.DoesNotExist:
                    return Response({
                        "status": 404,
                        "message": "Friend request not found",
                    })
            except Exception as e:
                    return Response({
                        "status": 500,
                        "message": str(e),
                    })

        @method_decorator(jwt_cookie_required)
        def delete(self, request):
            try :
                id = request.decoded_token['id']
                sender = Player.objects.get(id=id)
                receiver_id = request.data.get('target_id')
                receiver = Player.objects.get(id=receiver_id)
                friendship = Friendship.objects.get(sender=sender, receiver=receiver)
                friendship.delete()
                return Response({
                    "status": 200,
                    "message": 'Friendship deleted successfully'
                })
            except Friendship.DoesNotExist:
                return Response({
                    "status": 404,
                    "message": "Friend request not found",
                })
            except Exception as e:
                return Response({
                    "status": 500,
                    "message": str(e),
                })
