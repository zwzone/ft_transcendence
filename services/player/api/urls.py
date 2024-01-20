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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import PlayerUsernameView, PlayerLastNameView, \
    PlayerFirstNameView , PlayerInfoView , PlayerAvatarView

schema_view = get_schema_view(
    openapi.Info(
        title="Player API Documentation",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', PlayerInfoView.as_view(), name='playerView'),
    path('player/username', PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('player/first_name', PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('player/last_name', PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('player/avatar', PlayerAvatarView.as_view(), name='playerAvatarView'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
