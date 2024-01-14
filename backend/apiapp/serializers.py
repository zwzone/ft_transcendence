from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('username',)
class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('Avatar',)
