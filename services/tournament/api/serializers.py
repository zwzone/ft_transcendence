from rest_framework import serializers
from .models import Player, Tournament, PlayerMatch, Match, PlayerTournament
from django.db.models import Q


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'avatar', 'tournament_name')


class PlayerMatchSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = PlayerMatch
        fields = ('player', 'score')
    
    def get_player(self, player_match):
        player = Player.objects.get(id=player_match.player_id.id)
        serializer = PlayerSerializer(player)
        return serializer.data


class TournamentSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'status', 'round', 'matches', 'creator')

    def get_matches(self, tournament):
        matches = Match.objects.filter(tournament=tournament)
        serializer = MatchSerializer(matches, context={"player": self.context.get("player")}, many=True)
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

    def get_creator(self, tournament):
        player = self.context.get("player")
        return PlayerTournament.objects.filter(tournament_id=tournament, player_id=player, creator=True).exists()

class MatchSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()
    current = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ('id', 'game', 'state', 'round', 'current', 'players')

    def get_current(self, match):
        player = self.context.get("player")
        if match.state == Match.State.PLAYED.value:
            return False
        current_bool = PlayerMatch.objects.filter(match_id=match, player_id=player).exists()
        return current_bool

    def get_players(self, match):
        player_matches = PlayerMatch.objects.filter(match_id=match.id)
        serializer = PlayerMatchSerializer(player_matches, many=True)
        return serializer.data
