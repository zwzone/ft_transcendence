from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Player API Documentation",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.PlayerInfoView.as_view(), name='playerView'),
    path('username/', views.PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('first_name/', views.PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('last_name/', views.PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('avatar/', views.PlayerAvatarView.as_view(), name='playerAvatarView'),
    path('add_friend/', views.PlayerAddFriend.as_view(), name='playerAddFriendView'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]