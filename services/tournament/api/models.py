from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from enum import Enum
from rest_framework.exceptions import ValidationError
from .settings import COMPETITORS


class Player(AbstractBaseUser):

    class Status(Enum):
        ONLINE = 'ON'
        OFFLINE = 'OF'
        INGAME = 'IG'
    STATUS_CHOICES = [
        (Status.ONLINE.value, 'ONLINE'),
        (Status.OFFLINE.value, 'OFFLINE'),
        (Status.INGAME.value, 'INGAME')
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30, blank=False, null=False, unique=True)
    username = models.CharField(max_length=20, blank=False, null=False, unique=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    tournament_name = models.CharField(max_length=20, blank=False, null=True)
    avatar = models.URLField(blank=False, null=False)
    two_factor = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=Status.ONLINE.value)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'Player: [ email: {self.email}, username: {self.username} ]'


class Friendship(models.Model):

    class Status(Enum):
        ACCEPTED = 'AC'
        PENDING = 'PN'
    STATUS_CHOICES = [
        (Status.ACCEPTED.value, 'ACCEPTED'),
        (Status.PENDING.value, 'PENDING'),
    ]

    sender = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=Status.PENDING.value)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'


class Match(models.Model):

    class Game(Enum):
        PONG = "PO"
        TICTACTOE = "TC"

        @classmethod
        def choices(cls):
            return [(choice.value, choice.name) for choice in cls]

    game = models.CharField(max_length=2, choices=Game.choices(), null=False, blank=False)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=False)
    round = models.IntegerField(default=1) #fiha ni9ach



class PlayerMatch(models.Model):

    class Language(Enum):
        C = 'CC'
        CPP = 'CP'

        @classmethod
        def choices(cls):
            return [(choice.value, choice.name) for choice in cls]

    match_id = models.ForeignKey(Match, on_delete=models.CASCADE, null=False, blank=False)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE,  null=False, blank=False)
    score = models.IntegerField(default=0 ,null=False, blank=False)
    language = models.CharField(max_length=2, choices=Language.choices(), null=True, blank=False)
    executable_path = models.CharField(max_length=255, null=True, blank=False)
    won = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return f"Score: {self.score}"


class Tournament(models.Model):
    class StatusChoices(Enum):
        PENDING = 'PN'
        PROGRESS = 'PR'
        FINISHED = 'FN'

        @classmethod
        def choices(cls):
            return [(choice.value, choice.name) for choice in cls]

    ongoing_round = models.IntegerField(default=1) #fiha ni9ach
    status = models.CharField(max_length=2, choices=StatusChoices.choices(), default=StatusChoices.PENDING.value, null=False, blank=False)
    players = models.ManyToManyField(Player, blank=False)

    def clean(self):
        if self.players.count() > COMPETITORS:
            raise ValidationError("The maximum number of players allowed is 8.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tournament : {self.id}"