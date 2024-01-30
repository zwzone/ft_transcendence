from django.urls import path
from .views import (
    PlayerUsernameView,
    PlayerLastNameView,
    PlayerFirstNameView,
    PlayerInfoView,
    PlayerAvatarView,
    PlayerAddFriend,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Player API Documentation",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', PlayerInfoView.as_view(), name='playerView'),
    path('username/', PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('first_name/', PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('last_name/', PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('avatar/', PlayerAvatarView.as_view(), name='playerAvatarView'),
    path('add_friend/', PlayerAddFriend.as_view(), name='playerAddFriendView'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]