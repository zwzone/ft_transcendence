from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.TournamentView.as_view(), name='TournamentEndPoint'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
