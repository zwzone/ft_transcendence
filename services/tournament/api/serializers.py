from rest_framework import serializers
from .models import Player, Tournament, PlayerMatch, Match, PlayerTournament
from django.db.models import Q


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'email', 'tournament_name')


class PlayerTournamentSerializer(serializers.ModelSerializer):
    player_id = PlayerSerializer()

    class Meta:
        model = PlayerTournament
        fields = ('player_id', 'creator', 'tournament_id')


class PlayerMatchSerializer(serializers.ModelSerializer):
    player_id = PlayerSerializer()
    class Meta:
        model = PlayerMatch
        fields = ('player_id', 'match_id', 'score')


class TournamentSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'status', 'round', 'matches')

    def get_matches(self, tournament):
        matches = Match.objects.filter(tournament=tournament)
        serializer = MatchSerializer(matches, many=True)
        return serializer.data

    def get_players(self, tournament):
        tournament_data = {
            'id': tournament.id,
            'name': tournament.name,
            'status': tournament.status,
        }
        players_tournaments = PlayerTournament.objects.filter(tournament_id=tournament)
        serializer = PlayerTournamentSerializer(instance=players_tournaments, many=True)
        players_data = serializer.data
        players_data.append(tournament_data)
        return players_data

    def get_players_count(self, tournament):
        players_tournaments = PlayerTournament.objects.filter(tournament_id=tournament)
        serializer = players_tournaments.count()
        return serializer

    def is_player_in_tournament(self, player):
        tournament = Tournament.objects.filter(
            Q(playertournament__player_id=player) &
            (Q(status=Tournament.StatusChoices.PENDING.value) |
            Q(status=Tournament.StatusChoices.PROGRESS.value))
        ).first()
        return tournament


class MatchSerializer(serializers.ModelSerializer):
    player_matches = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ('id', 'game', 'tournament', 'round', 'player_matches')

    def get_player_matches(self, match):
        player_matches = PlayerMatch.objects.filter(match_id=match.id)[:2]
        serializer = PlayerMatchSerializer(instance=player_matches, many=True)
        return serializer.data
