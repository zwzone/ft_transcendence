from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tournament, Player, Match, PlayerMatch, PlayerTournament
from .serializers import TournamentSerializer
from .settings import COMPETITORS, ROUNDS
from .decorators import jwt_cookie_required
from itertools import cycle, islice
from django.db.models import Q


def update_tournament(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    # tournament.status = Tournament.StatusChoices.PENDING.value
    # tournament.ongoing_round = 1
    # tournament.save()

    if tournament.status == Tournament.StatusChoices.FINISHED.value:
        return
    if tournament.ongoing_round >= ROUNDS:
        tournament.status = Tournament.StatusChoices.FINISHED.value
        tournament.save()
        return
    last_completed_round = tournament.ongoing_round - 1
    for round_num in range(1, ROUNDS):
        if round_num == last_completed_round:
            current_round_matches = Match.objects.filter(tournament=tournament, round=round_num)
            next_round_matches = Match.objects.filter(tournament=tournament, round=round_num + 1)
            for match in current_round_matches:
                winning_player_match = PlayerMatch.objects.filter(match=match, won=True).first()
                if winning_player_match:
                    next_match_query = Q(tournament=tournament, round=round_num + 1)
                    next_match_query &= Q(id=match.id // 2)
                    next_match = next_round_matches.filter(next_match_query).first()

                    if next_match:
                        if match.id % 2 == 1:
                            next_match.player1 = winning_player_match.player
                        else:
                            next_match.player2 = winning_player_match.player
                        next_match.save()
    if round_num == last_completed_round:
        tournament.ongoing_round += 1
    tournament.save()


class TournamentView(APIView):

    @jwt_cookie_required
    def get(self, request):
        target_id = request.query_params.get('target_id')
        if target_id is not None:
            try:
                tournament = Tournament.objects.get(id=target_id)
                serializer = TournamentSerializer(tournament)
                return Response({"status": 200, "tournament": serializer.data})
            except Tournament.DoesNotExist:
                return Response({"status": 404, "message": "Tournament not found"})
        tournaments = Tournament.objects.filter(status='PN')
        if tournaments is None:
            return Response({"status": 404, "message": "No Tournaments were available"})
        serializer = TournamentSerializer(tournaments, many=True)
        return Response({"status": 200, "tournaments": serializer.data})

    @jwt_cookie_required
    def post(self, request):
        action = request.data.get('action')
        player_id = request.decode_token['id']
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"status": 400, "message": "Player does not exist"})
        serializer = TournamentSerializer()
        if "create" in action:
            name = request.data.get('name')
            if name is None or len(name) == 0:
                return Response({"status": 400, "message": "Invalid Tournament name"})
            if serializer.is_player_in_pending_tournament(player) :
                return Response({"status": 400, "message": "Already in a Tournament"})
            tournament = Tournament.objects.create(name=name)
            PlayerTournament.objects.create(player_id=player, tournament_id=tournament, creator=True)
            serializer = TournamentSerializer(tournament)
            return Response({"status": 201, "curret_tournament": serializer.data}, status=201)
        elif "join" in action:
            tournament_id = request.data.get('tournament_id')
            if tournament_id is None or len(tournament_id) == 0:
                return Response({"status": 400, "message": "Missing Tournament id"})
            try:
                tournament = Tournament.objects.get(id=tournament_id)
                serializer = TournamentSerializer(tournament)
            except Tournament.DoesNotExist:
                return Response({"status": 404, "message": "Tournament not found"})
            if tournament.status == 'PN' or serializer.get_players_count(tournament) != COMPETITORS:
                player_id = request.decode_token['id']
                player = Player.objects.get(id=player_id)
                if serializer.is_player_in_pending_tournament(player):
                    return Response({"status": 400, "message": "Already in a Tournament"})
                PlayerTournament.objects.create(player_id=player, tournament_id=tournament)
                return Response({"status": 200, "message": "Successfully joined tournament"})
            return Response({"status": 400, "message": "Tournament is full"})
        elif "leave" in action:
            tournament_id = request.data.get('tournament_id')
            if tournament_id is None or len(tournament_id) == 0:
                return Response({"status": 400, "message": "Missing Tournament id"})
            try:
                tournament = Tournament.objects.get(id=tournament_id)
            except Tournament.DoesNotExist:
                return Response({"status": 400, "message": "Tournament does not exist"})
            if tournament.status != Tournament.StatusChoices.PENDING.value:
                return Response({"status": 400, "message": "Tournament status is not pending"})
            player_id = request.decode_token['id']
            try:
                player = Player.objects.get(id=player_id)
            except Player.DoesNotExist:
                return Response({"status": 400, "message": "Player does not exist"})
            try:
                player_tournament = PlayerTournament.objects.get(player_id=player, tournament_id=tournament)
            except PlayerTournament.DoesNotExist:
                return Response({"status": 400, "message": "Player is not in the Tournament"})
            if player_tournament.creator:
                tournament.delete()
                return Response({"status": 200, "message": "Tournament deleted along with player"})
            else:
                player_tournament.delete()
                return Response({"status": 200, "message": "Player removed from Tournament"})
        elif "start" in action:
            tournament_id = request.data.get('tournament_id')
            if tournament_id is None or len(tournament_id) == 0:
                return Response({"status": 400, "message": "Missing Tournament id"})
            tournament = Tournament.objects.get(id=tournament_id)
            serializer = TournamentSerializer(tournament)
            player_id = request.decode_token['id']
            try:
                player = Player.objects.get(id=player_id)
            except Player.DoesNotExist:
                return Response({"status": 400, "message": "Player does not exist"})
            if not PlayerTournament.objects.filter(player_id=player, tournament_id=tournament, creator=True).exists():
                return Response({"status": 400, "message": "Tournament cannot be started"})
            if serializer.get_players_count(tournament) != COMPETITORS:
                return Response({"status": 400, "message": "Tournament not full yet"})
            if tournament.status == Tournament.StatusChoices.PENDING.value:
                players_tournaments = PlayerTournament.objects.filter(tournament_id=tournament)
                players_cycle = cycle(players_tournaments)
                for i in range(0, COMPETITORS - 1, 2):
                    player1 = next(players_cycle).player_id
                    player2 = next(players_cycle).player_id
                    tournament_match = Match.objects.create(
                        tournament=tournament,
                        game=Match.Game.PONG.value,
                        round=tournament.round
                    )
                    PlayerMatch.objects.create(
                        match_id=tournament_match,
                        player_id=player1
                    )
                    PlayerMatch.objects.create(
                        match_id=tournament_match,
                        player_id=player2
                    )
                tournament.status = Tournament.StatusChoices.PROGRESS.value
                tournament.save()
                return Response({"status": 200, "message": "Tournament started",
                                 "tournament_id": tournament_id})
            return Response({"status": 400, "message": "Tournament is not pending"})
        return Response({"status": 400, "message": "Wrong Action"})
