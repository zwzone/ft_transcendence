from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Player, PlayerMatch
from .decorators import jwt_cookie_required

class LastMatchesView(APIView):

    @method_decorator(jwt_cookie_required)
    def get(self, request):
        try:
            player = Player.objects.get(id=request.decoded_token['id'])
            matches = PlayerMatch.objects.filter(player_id=player).order_by('-match_id__id')[:8]
            matches_data = []
            for match in matches:
                opponent = match.match_id.playermatch_set.exclude(player_id=player).first().player_id
                matches_data.append({
                    "id": match.match_id.id,
                    "game": match.match_id.game,
                    "score": match.score,
                    "won": match.won,
                    "opponent": opponent.username,
                })
            return Response({
                "status": 200,
                "matches": matches_data
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