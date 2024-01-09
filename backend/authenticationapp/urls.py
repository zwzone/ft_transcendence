from django.urls import path

from authenticationapp.views import intra_auth_api, intra_redirect_api

urlpatterns = [
    path('auth/', intra_auth_api, name='authAPI'),
    path('redirect/', intra_redirect_api, name='redirectAPI'),
]