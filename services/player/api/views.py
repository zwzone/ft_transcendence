from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlayerSerializer, UsernameSerializer, FirstNameSerializer, LastNameSerializer
from .models import Player
import jwt
from jwt.exceptions import ExpiredSignatureError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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

# this is commented out because it is not used right now

# class UserByUsernameView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request, username):
#         try:
#             user = Player.objects.get(username=username)
#             serializer = PlayerSerializer(user)
#             return Response({
#                 "status": 200,
#                 "user": serializer.data
#             })
#         except Player.DoesNotExist:
#             return Response({
#                 "status": 404,
#                 "message": "User not found",
#             })


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
