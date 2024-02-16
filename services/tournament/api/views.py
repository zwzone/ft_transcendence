import math
from rest_framework.decorators import api_view
import random
from rest_framework.response import Response
from .models import Tournament, Player, Match
from .serializers import TournamentSerializer
from .settings import COMPETITORS, ROUNDS
from .decorators import jwt_cookie_required


def update_tournament(tournament_id):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.ongoing_round > ROUNDS:
        lobby.over = True
        lobby.save()
        return
    if lobby.players.count() == COMPETITORS:
        lobby.status = Tournament.StatusChoices.IN_PROGRESS.value
        lobby.save()
        return
    for round_num in range(1, ROUNDS):
        current_round_matches = Match.objects.filter(tournament=tournament_id, round=round_num)
        next_round_matches = Match.objects.filter(tournament=tournament_id, round=round_num + 1)
        for match in current_round_matches:
            if match.qualified:
                next_match = next_round_matches.get(id=math.ceil(match.id / 2))
                if match.id % 2 == 1:
                    next_match.player1 = match.qualified
                else:
                    next_match.player2 = match.qualified
                next_match.save()
    return


@api_view(['POST'])
@jwt_cookie_required
def create_tournament(request):
    user_id = request.decoded_token['id']  
    join_code = user_id * 1000 + random.randint(1, 999)
    if Tournament.objects.filter(id=join_code).exists():
        return Response({"status": 400, "message": "Join code already exists"})
    lobby = Tournament.objects.create(id=join_code)
    serializer = TournamentSerializer(lobby)
    return Response(serializer.data, status=201)


@api_view(['POST'], )
def join_tournament(tournament_id, request):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.players.count() >= COMPETITORS or lobby.status != Tournament.StatusChoices.PENDING.value:
        return Response({"status": 400, "message": "Tournament is full"})
    player = Player.objects.get(id = request.decode_token['id'])
    lobby.players.add(player)
    lobby.save()
    return Response({"status": 200, "message": "successfully joined tournament"})


@api_view(['GET'])
def get_tournaments(tournament_id, request):
    try:
        update_tournament(tournament_id)
        lobby = Tournament.objects.get(id=tournament_id)
        serializer = TournamentSerializer(lobby)
        return Response(serializer.data)
    except Tournament.DoesNotExist:
        return Response({"status": 404, "message": "Tournament not found"})


@api_view(['POST'], )
def start_tournament(tournament_id, request):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.players.count() != COMPETITORS:
        return Response({"status": 400, "message": "Tournament not full"})
    lobby.status = Tournament.StatusChoices.IN_PROGRESS.value
    for i in range(0, COMPETITORS - 1, 2):
        tournament_match = Match.objects.create(player1=lobby.players.all()[i],
                                                player2=lobby.players.all()[i + 1],id=i//2+ 1)
        lobby.matches.add(tournament_match)
    for i in range(2, ROUNDS + 1):
        for j in range(0, math.ceil(COMPETITORS / (2 ** (i - 1))), 2):
            match = lobby.objects.create(round=i, id=j//2+1)
            lobby.matches.add(match)
    return Response({"status": 200, "message": "Tournament started", "tournament_id": tournament_id})


@api_view(['DELETE'], )
@jwt_cookie_required
def leave_tournament(tournament_id, request):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.status == Tournament.StatusChoices.PENDING.value:
        player = Player.objects.get(id = request.decode_token['id'])
        lobby.players.get(player)
        lobby.players.remove(player)
        return Response({"status": 200, "message": "player removed"})
    return Response({"status": 400, "message": "Player can't leave Tournament"})
