from rest_framework import serializers
from .models import Player, Tournament


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'tournament_name')


class TournamentSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'status', 'players', 'current_round')
