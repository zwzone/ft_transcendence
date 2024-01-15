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

class FirstNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('first_name',)
        
class LastNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('last_name',)
#this comment below is for future use
# class AvatarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Player
#         fields = ('avatar',)
