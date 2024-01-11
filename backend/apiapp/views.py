from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def player(request):
    return Response("This is the player")
