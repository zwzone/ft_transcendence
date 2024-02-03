from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PlayerInfo.as_view(), name='playerInfoView'),
    path('avatar/', views.PlayerAvatarUpload.as_view(), name='playerAvatarUploadView'),
    path('add_friend/', views.PlayerAddFriend.as_view(), name='playerAddFriendView'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
