from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):
    email = models.EmailField(max_length=30, blank=False, null=False, unique=True)
    username = models.CharField(max_length=20, blank=False, null=False, unique=True)
    tournament_name = models.CharField(max_length=20, blank=False, null=True)

    def __str__(self):
        return self.email
