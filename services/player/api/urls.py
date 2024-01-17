"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import PlayerUsernameView, PlayerLastNameView, \
    PlayerFirstNameView , PlayerInfoView , PlayerAvatarView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', PlayerInfoView.as_view(), name='playerView'),
    path('player/username', PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('player/first_name', PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('player/last_name', PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('player/avatar', PlayerAvatarView.as_view(), name='playerAvatarView'),
]
