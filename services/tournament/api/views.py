from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tournament, Player, Match, PlayerMatch, PlayerTournament
from .serializers import TournamentSerializer
from .settings import COMPETITORS, ROUNDS
from .decorators import jwt_cookie_required
from itertools import cycle


def update_tournament(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.status == Tournament.StatusChoices.FINISHED.value:
        return
    current_round = tournament.round
    current_round_matches = Match.objects.filter(tournament=tournament, round=current_round)
    if all(match.state == Match.State.PLAYED.value for match in current_round_matches):
        if tournament.round == 3:
            tournament.status = Tournament.StatusChoices.FINISHED.value
            tournament.save()
            return
        winning_players = list(PlayerMatch.objects.filter(match_id__in=current_round_matches, won=True))
        while len(winning_players) >= 2:
            player1_match = winning_players.pop(0)
            player2_match = winning_players.pop(0)
            player1 = player1_match.player_id
            player2 = player2_match.player_id
            tournament_match = Match.objects.create(
                tournament=tournament,
                game=Match.Game.PONG.value,
                round=current_round + 1
            )
            PlayerMatch.objects.create(
                match_id=tournament_match,
                player_id=player1
            )
            PlayerMatch.objects.create(
                match_id=tournament_match,
                player_id=player2
            )
            tournament.round += 1
            tournament.save()


class TournamentView(APIView):

    @method_decorator(jwt_cookie_required)
    def get(self, request):
        player_id = request.decoded_token['id']
        serializer = TournamentSerializer()
        player = Player.objects.get(id=player_id)
        if serializer.is_player_in_tournament(player):
            try:
                tournament = serializer.is_player_in_tournament(player)
                serializer = TournamentSerializer(tournament, context={"player": player})
                if tournament.status == Tournament.StatusChoices.PENDING.value:
                    return Response({"status": 200, "current_tournament": serializer.data, "players": serializer.get_players(tournament)})
                update_tournament(tournament.id)
                return Response({"status": 200, "current_tournament": serializer.data})
            except Tournament.DoesNotExist:
                return Response({"status": 404, "message": "Tournament not found"})
        tournaments = Tournament.objects.filter(status='PN')
        player_finished_tournament = PlayerTournament.objects.filter(player_id=player).order_by('-id').first()
        response_data = {}
        if player_finished_tournament is not None:
            finished_tournament = Tournament.objects.filter(id=player_finished_tournament.tournament_id.id).first()
            serializer_finished = TournamentSerializer(finished_tournament)
            response_data["current_tournament"] = serializer_finished.data
        if not tournaments:
            response_data.update({"status": 404, "message": "No Tournaments are available"})
            return Response(response_data)
        serializer_all = TournamentSerializer(tournaments, many=True)
        response_data.update({"status": 200, "tournaments": serializer_all.data})
        return Response(response_data)

    @method_decorator(jwt_cookie_required)
    def post(self, request):
        action = request.data.get('action')
        tournament_id = request.data.get('tournament_id')
        name = request.data.get('tournament_name')
        alias = request.data.get('alias_name')
        player_id = request.decoded_token['id']
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"status": 400, "message": "Player does not exist"})
        if "create" in action:
            if name is None or len(name) == 0 or alias is None or len(alias) == 0:
                return Response({"status": 400, "message": "Invalid Tournament name"})
            serializer = TournamentSerializer()
            if serializer.is_player_in_tournament(player):
                return Response({"status": 400, "message": "Already in a Tournament"})
            tournament = Tournament.objects.create(name=name)
            PlayerTournament.objects.create(player_id=player, tournament_id=tournament, creator=True)
            serializer = TournamentSerializer(tournament)
            player.tournament_name = alias
            player.save()
            return Response({"status": 201, "current_tournament": serializer.get_players(tournament)}, status=201)
        try:
            tournament = Tournament.objects.get(id=tournament_id)
            serializer = TournamentSerializer(tournament)
        except Tournament.DoesNotExist:
            return Response({"status": 404, "message": "Not found"})
        if "join" in action:
            if tournament_id is None or len(tournament_id) == 0 or alias is None or len(alias) == 0:
                return Response({"status": 400, "message": "Missing Tournament id"})
            if tournament.status == 'PN' and serializer.get_players_count(tournament) < COMPETITORS:
                if serializer.is_player_in_tournament(player):
                    return Response({"status": 400, "message": "Already in a Tournament"})
                player.tournament_name = alias
                player.save()
                PlayerTournament.objects.create(player_id=player, tournament_id=tournament)
                return Response({"status": 200, "message": "Successfully joined tournament"})
            return Response({"status": 400, "message": "Tournament is full"})
        elif "leave" in action:
            if tournament.status != Tournament.StatusChoices.PENDING.value:
                return Response({"status": 400, "message": "Tournament status is not pending"})
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
