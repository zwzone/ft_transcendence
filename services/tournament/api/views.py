import math
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tournament, Player, Match, PlayerMatch
from .serializers import TournamentSerializer
from .settings import COMPETITORS, ROUNDS
from .decorators import jwt_cookie_required
from random import shuffle
from itertools import cycle, islice
from django.db.models import Q


def update_tournament(tournament_id):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.status == Tournament.StatusChoices.FINISHED.value:
        return
    if lobby.ongoing_round >= ROUNDS:
        lobby.status = Tournament.StatusChoices.FINISHED.value
        lobby.save()
        return
    last_completed_round = lobby.ongoing_round - 1
    for round_num in range(1, ROUNDS):
        if round_num == last_completed_round:
            current_round_matches = Match.objects.filter(tournament=lobby, round=round_num)
            next_round_matches = Match.objects.filter(tournament=lobby, round=round_num + 1)

            for match in current_round_matches:
                winning_player_match = PlayerMatch.objects.filter(match=match, won=True).first()
                if winning_player_match:
                    next_match_query = Q(tournament=lobby, round=round_num + 1)
                    next_match_query &= Q(id=match.id // 2)
                    next_match = next_round_matches.filter(next_match_query).first()

                    if next_match:
                        if match.id % 2 == 1:
                            next_match.player1 = winning_player_match.player
                        else:
                            next_match.player2 = winning_player_match.player
                        next_match.save()
    lobby.ongoing_round += 1
    lobby.save()



@api_view(['POST'])
@jwt_cookie_required
def create_tournament(request):
    player_id = request.decoded_token['id']
    player = Player.objects.get(id=player_id)
    if Tournament.objects.filter(players=player, status=Tournament.StatusChoices.PENDING.value).exists():
        return Response({"status": 400, "message": "Already in a Tournament"})
    lobby = Tournament.objects.create()
    lobby.players.add(player)
    serializer = TournamentSerializer(lobby)
    return Response(serializer.data, status=201)


@api_view(['POST'])
@jwt_cookie_required
def join_tournament(tournament_id, request):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.players.count() >= COMPETITORS or lobby.status != Tournament.StatusChoices.PENDING.value:
        return Response({"status": 400, "message": "Tournament is full"})
    player = Player.objects.get(id = request.decode_token['id'])
    lobby.players.add(player)
    lobby.save()
    return Response({"status": 200, "message": "successfully joined tournament"})


@api_view(['GET'])
@jwt_cookie_required
def get_tournaments(request):
    tournaments = Tournament.objects.filter(status='PN')
    if tournaments is None:
        return Response({"staus": 404, "message": "No Tournaments were availble"})
    serializer = TournamentSerializer(tournaments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@jwt_cookie_required
def get_tournament_by_id(tournament_id, request):
    try:
        update_tournament(tournament_id)
        lobby = Tournament.objects.get(id=tournament_id)
        serializer = TournamentSerializer(lobby)
        return Response(serializer.data)
    except Tournament.DoesNotExist:
        return Response({"status": 404, "message": "Tournament not found"})


@api_view(['POST'])
@jwt_cookie_required
def start_tournament(request, tournament_id):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.players.count() != COMPETITORS:
        return Response({"status": 400, "message": "Tournament not full"})
    shuffle(lobby.players)
    player_list = list(lobby.players.all())
    lobby.status = Tournament.StatusChoices.PROGRESS.value
    players_cycle = cycle(player_list)
    for i in range(0, COMPETITORS - 1, 2):
        player1, player2 = islice(players_cycle, 2)
        tournament_match = Match.objects.create(
            tournament=lobby,
            game=Match.Game.PONG.value,
            round=i
        )
        PlayerMatch.objects.create(
            match_id=tournament_match.id,
            player_id=player1.id
        )
        PlayerMatch.objects.create(
            match_id=tournament_match.id,
            player_id=player2.id
        )
    lobby.save()
    return Response({"status": 200, "message": "Tournament started", "tournament_id": tournament_id})


@api_view(['DELETE'])
@jwt_cookie_required
def leave_tournament(tournament_id, request):
    lobby = Tournament.objects.get(id=tournament_id)
    if lobby.status == Tournament.StatusChoices.PENDING.value:
        player = Player.objects.get(id = request.decode_token['id'])
        lobby.players.get(player)
        lobby.players.remove(player)
        return Response({"status": 200, "message": "player removed"})
    return Response({"status": 400, "message": "Player can't leave Tournament"})
