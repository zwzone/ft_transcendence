from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    display_name = models.CharField(max_length=50, blank=False, null=True)
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.username
