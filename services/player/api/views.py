from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlayerSerializer, UsernameSerializer, FirstNameSerializer, LastNameSerializer
import jwt
from jwt.exceptions import ExpiredSignatureError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Player, Friendship
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(request_body=PlayerSerializer)
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({
                "message": "JWT token not found",
            }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if 'email' in decoded_token:
                email = decoded_token['email']
                player = request.data.get('player')
                username = player['username']
                first_name = player['first_name']
                last_name = player['last_name']
                avatar = player['avatar']
            player, created = Player.objects.get_or_create(email=email, username=username, first_name=first_name,
                                                           last_name=last_name, avatar=avatar)
            if created:
                return Response({
                    "message": "User created successfully",
                    "id": player.id,
                    "two_factor": player.two_factor
                }, status=status.HTTP_201_CREATED)
            elif created is False and player is not None:
                return Response({
                    "message": "User already exists",
                    "id": player.id,
                    "two_factor": player.two_factor,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlayerLastNameView(APIView):
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
            return Response({
                "status": 200,
                "last_name": user.last_name
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

    @swagger_auto_schema(request_body=LastNameSerializer)
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
            user = Player.objects.get(id=id)
            last_name = request.data.get('last_name')
            if not last_name:
                return Response({
                    "status": 400,
                    "message": "Last name not provided",
                })
            user.last_name = last_name
            user.save()
            serializer = PlayerSerializer(user)
            return Response({
                "status": 200,
                "message": "Last name updated successfully",
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


class PlayerUsernameView(APIView):
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
            return Response({
                "status": 200,
                "username": user.username
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

    @swagger_auto_schema(request_body=UsernameSerializer)
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
                "message": "Username updated successfully",
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


class PlayerAvatarView(APIView):
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
            return Response({
                "status": 200,
                "avatar": user.avatar
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
                "message": "what" + str(e),
            })

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
            user = Player.objects.get(id=id)

            avatar_file = request.FILES.get('avatar')

            if avatar_file:
                file_name = default_storage.save(avatar_file.name, avatar_file)
                file_url = default_storage.url(file_name)
                user.Avatar = file_url
                user.save()

                return Response({
                    "status": 200,
                    "message": "Avatar uploaded successfully",
                    "avatar_url": file_url
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


class PlayerFirstNameView(APIView):
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
            return Response({
                "status": 200,
                "first_name": user.first_name
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

    @swagger_auto_schema(request_body=FirstNameSerializer)
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
            user = Player.objects.get(id=id)
            first_name = request.data.get('first_name')
            if not first_name:
                return Response({
                    "status": 400,
                    "message": "First name not provided",
                })
            user.first_name = first_name
            user.save()
            serializer = PlayerSerializer(user)
            return Response({
                "status": 200,
                "message": "First name updated successfully",
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


#this is my model for the friend request 
# class Player(AbstractUser):
#     email = models.EmailField(max_length=30, blank=False, null=False)
#     first_name = models.CharField(max_length=20, blank=False, null=False)
#     last_name = models.CharField(max_length=20, blank=False, null=False)
#     username = models.CharField(max_length=20, blank=False, null=False, unique=True)
#     avatar = models.URLField(blank=True, null=True)
#     id = models.AutoField(primary_key=True)

#     def __str__(self):
#         return self.email

# class Friendship(models.Model):
#     sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_friend_requests')
#     receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_friend_requests')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.sender.username} -> {self.receiver.username}' so this is the model for the friend request

class PlayerAddFriend(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(request_body=FirstNameSerializer)
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

# class UpdateAvatarView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     @swagger_auto_schema(methods=['post'], request_body=AvatarSerializer)
#     def post(self, request):
#         token = request.COOKIES.get('jwt_token')
#         if not token:
#             return Response({
#                 "status": 401,
#                 "message": "JWT token not found in cookies",
#             })

#         try:
#             decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             id = decoded_token['id']
#             user = Player.objects.get(id=id)

#             avatar_file = request.FILES.get('avatar')

#             if avatar_file:
#                 file_path = os.path.join(settings.MEDIA_ROOT, f"avatars/{id}")
#                 default_storage.save(file_path, ContentFile(avatar_file.read()))
#                 user.Avatar = file_path
#                 user.save()

#                 return Response({
#                     "status": 200,
#                     "message": "Avatar uploaded successfully",
#                 })
#             else:
#                 return Response({
#                     "status": 400,
#                     "message": "Avatar file not provided",
#                 })

#         except Player.DoesNotExist:
#             return Response({
#                 "status": 404,
#                 "message": "User not found",
#             })
#         except Exception as e:
#             return Response({
#                 "status": 500,
#                 "message": "Error: " + str(e),
#             })
