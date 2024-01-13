from django.db import models
from rest_framework import serializers
from typing import Dict
import jwt


class GoogleRawLoginCredentials(models.Model):
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)

class GoogleAccessTokens(models.Model):
    id_token = models.TextField()
    access_token = models.TextField()

    def decode_id_token(self) -> Dict[str, str]:
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        return decoded_token

class GoogleRawLoginCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleRawLoginCredentials
        fields = ['client_id', 'client_secret', 'project_id']

class GoogleAccessTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAccessTokens
        fields = ['id_token', 'access_token']
