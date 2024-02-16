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

    game = models.CharField(max_length=2, choices=Game.choices())
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player1", blank=True, null=True)
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player2", blank=True, null=True)
    qualified = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="qualified", blank=True, null=True)
    round = models.IntegerField(default=1)

    def __str__(self):
        return self.player1.name + " vs " + self.player2.name


class Tournament(models.Model):
    class StatusChoices(Enum):
        PENDING = 'PE'
        IN_PROGRESS = 'IP'
        FINISHED = 'FI'

        @classmethod
        def choices(cls):
            return [(choice.value, choice.name) for choice in cls]

    players = models.ManyToManyField(Player, blank=True)
    ongoing_round = models.IntegerField(default=1)
    matches = models.ManyToManyField(Match, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices(), default=StatusChoices.PENDING.value)
    over = models.BooleanField(default=False)

    def clean(self):
        if self.players.count() > COMPETITORS:
            raise ValidationError("The maximum number of players allowed is 8.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tournament : {self.id}"
