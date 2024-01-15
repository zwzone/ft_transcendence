from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlayerSerializer, UsernameSerializer
from .models import Player
import jwt
from jwt.exceptions import ExpiredSignatureError


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
        authentication_classes = []
        permission_classes = []
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
            last_name = request.data.get('last_name')
            tournament_name = request.data.get('tournament_name')
            if not first_name:
                return Response({
                    "status": 400,
                    "message": "First name not provided",
                })
            if not last_name:
                return Response({
                    "status": 400,
                    "message": "Last name not provided",
                })
            if not tournament_name:
                return Response({
                    "status": 400,
                    "message": "Tournament name not provided",
                })
            user.first_name = first_name
            user.last_name = last_name
            user.tournament_name = tournament_name
            user.save()
            serializer = PlayerSerializer(user)
            return Response({
                "status": 200,
                "message": "User info updated successfully",
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
                "avatar": user.Avatar
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
