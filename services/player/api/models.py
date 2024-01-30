from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class Player(AbstractUser):
    email = models.EmailField(max_length=30, blank=False, null=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    username = models.CharField(max_length=20, blank=False, null=False, unique=True)
    avatar = models.URLField(blank=True, null=True)
    id = models.AutoField(primary_key=True)
    two_factor = models.BooleanField(default=False)

    def __str__(self):
        return self.email



class Friendship(models.Model):
    STATUS_CHOICES = [
        (FriendshipStatus.ACCEPTED.value, 'Accepted'),
        (FriendshipStatus.PENDING.value, 'Pending'),
    ]

    sender = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=FriendshipStatus.PENDING.value)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

# Here we define any custom enums we want to use

class FriendshipStatus(Enum):
    ACCEPTED = 'accepted'
    PENDING = 'pending'