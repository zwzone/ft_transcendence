from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from enum import Enum


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
