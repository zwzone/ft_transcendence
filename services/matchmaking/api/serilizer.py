from rest_framework import serializers
from .models import PlayerMatch, Match

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'score']

class PlayerMatchSerializer(serializers.ModelSerializer):
    match = MatchSerializer()  # Nested serializer to include match details
    
    class Meta:
        model = PlayerMatch
        fields = ['id', 'match', 'player_id', 'score', 'language', 'executable_path', 'won']