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
    path('add_friend/', views.PlayerAddFriend.as_view(), name='playerAddFriendView'),
]
