from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    tournament_name = models.CharField(max_length=50, blank=False, null=True)

    # USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
