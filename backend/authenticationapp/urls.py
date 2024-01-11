from django.urls import path

from authenticationapp.views import intra_auth, callback_auth

urlpatterns = [
    path('intra/', intra_auth, name='intraView'),
    path('callback/', callback_auth, name='callbackView'),
]
