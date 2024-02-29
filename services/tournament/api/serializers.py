from rest_framework import serializers
from .models import Player, Tournament, PlayerMatch, Match, PlayerTournament
from django.db.models import Q


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('avatar', 'tournament_name')


class PlayerMatchSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = PlayerMatch
        fields = ('player', 'score')
    
    def get_player(self, player_id):
        player = Player.objects.get(id=player_id.id)
        serializer = PlayerSerializer(player)
        return serializer.data


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
        players_tournaments = PlayerTournament.objects.filter(tournament_id=tournament)
        players = []
        for player_tournament in players_tournaments:
            players.append(Player.objects.get(id=player_tournament.player_id.id))
        player_data = PlayerSerializer(instance=players, many=True)
        return player_data.data

    def get_players_count(self, tournament):
        players_tournaments = PlayerTournament.objects.filter(tournament_id=tournament)
        return players_tournaments.count()

    def is_player_in_tournament(self, player):
        tournament = Tournament.objects.filter(
            Q(playertournament__player_id=player) &
            (Q(status=Tournament.StatusChoices.PENDING.value) |
            Q(status=Tournament.StatusChoices.PROGRESS.value))
        ).first()
        return tournament

    def get_creator(self, tournament, player):
        creator = PlayerTournament.objects.filter(tournament_id=tournament, player_id=player, creator=True).first()
        return creator

class MatchSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ('id', 'game', 'state', 'round', 'matches')

    def get_matches(self, match):
        player_matches = PlayerMatch.objects.filter(match_id=match.id)[:2]
        serializer = PlayerMatchSerializer(instance=player_matches, many=True)
        return serializer.data
