from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):
    email = models.EmailField(max_length=30, blank=False, null=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    username = models.CharField(max_length=20, blank=False, null=False, unique=True)
    avatar = models.URLField(blank=True, null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.email
