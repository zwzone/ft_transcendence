from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlayerInfoSerializer
from .models import Player, Friendship
from .decorators import jwt_cookie_required
import urllib.parse
import os


class PlayerInfo(APIView):

    @method_decorator(jwt_cookie_required)
    def get(self, request):
        try:
            username = request.query_params.get('username')
            if username:
                player = Player.objects.get(username=username)
                serializer = PlayerInfoSerializer(player)
                return Response({
                    "status": 200,
                    "players": serializer.data,
                    "message": "User found successfully"
                })
            player = Player.objects.get(id=request.decoded_token['id'])
            serializer = PlayerInfoSerializer(player)
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
        try:
            changed = False
            id = request.decoded_token['id']
            player_data = request.data.get('player')
            player = Player.objects.get(id=id)
            if "username" in player_data:
                username = ' '.join(player_data["username"].split())
                if not username or len(player_data['username']) > 8 :
                    return Response({
                        "status": 400,
                        "message": "Invalid username",
                    })
                player.username = username
                changed = True
            if "first_name" in player_data:
                first_name = ' '.join(player_data['first_name'].split())
                if not first_name or len(first_name) > 20 :
                    return Response({
                        "status": 400,
                        "message": "Invali first name",
                    })
                player.first_name = first_name
                changed = True
            if "last_name" in player_data:
                last_name = ' '.join(player_data['last_name'].split())
                if not last_name or len(last_name) > 20 :
                    return Response({
                        "status": 400,
                        "message": "Invalid last name",
                    })
                player.last_name = last_name
                changed = True
            if "two_factor" in player_data and player_data['two_factor'] is False:
                player.two_factor = player_data['two_factor']
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
                if get_type == 'invites':
                    friendships = Friendship.objects.filter(receiver=id, status='PN')
                    friendship_data = []
                    for friendship in friendships:
                        friend = friendship.sender
                        friend_data = {
                            "id": friend.id,
                            "first_name": friend.first_name,
                            "last_name": friend.last_name,
                            "username": friend.username,
                            "status": friend.status,
                            "tournament_name": friend.tournament_name,
                            "two_factor": friend.two_factor,
                            "avatar": friend.avatar
                            
                        }
                        friendship_data.append(friend_data)
                    return Response({
                        "status": 200,
                        "friendships": friendship_data
                    })
                elif get_type == 'friends':
                    friendships = Friendship.objects.filter(status='AC')
                    friendship_data = []
                    encountered_usernames = [] 
                    for friendship in friendships:
                        sender_username = friendship.sender.username
                        receiver_username = friendship.receiver.username
                        
                        if sender_username not in encountered_usernames:
                            friend_data = {
                                "username": sender_username,
                                "avatar": friendship.sender.avatar
                            }
                            friendship_data.append(friend_data)
                            encountered_usernames.append(sender_username)
                        
                        if receiver_username not in encountered_usernames:
                            friend_data = {
                                "id": friendship.receiver.id,
                                "username": receiver_username,
                                "first_name": friendship.receiver.first_name,
                                "last_name": friendship.receiver.last_name,
                                "avatar": friendship.receiver.avatar,
                                "status": friendship.recevier.status,
                                "tounament_name": friendship.receiver.tournament_name,
                                "two_factor": friendship.receiver.two_factor
                            }
                            friendship_data.append(friend_data)
                            encountered_usernames.append(receiver_username)

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
                            "id": friend.id,
                            "username": friend.username,
                            "first_name": friend.first_name,
                            "last_name": friend.last_name,
                            "status": friend.status,
                            "tournament_name": friend.tournament_name,
                            "avatar": friend.avatar,
                            "two_factor": friend.two_factor
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
            id = request.decoded_token['id']
            sender = Player.objects.get(id=id)
            receiver_id = request.data.get('target_id')
            receiver = Player.objects.get(id=receiver_id)
            friendship = Friendship.objects.get(sender=sender, receiver=receiver)
            if friendship is None:
                try :
                    friendship = Friendship.objects.get(sender=receiver, receiver=sender)
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
