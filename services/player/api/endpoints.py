from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerInfoView.as_view(), name='playerView'),
    path('username/', views.PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('first_name/', views.PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('last_name/', views.PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('avatar/', views.PlayerAvatarView.as_view(), name='playerAvatarView'),
]
