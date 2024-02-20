from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='TournamentIndex'),
    path('', views.create_tournament, name='CreateTournament'),
    path('tournament/<int:tournament_id>/', views.get_tournaments, name='GetTournament'),
    path('tournament/<int:tournament_id>/join/', views.join_tournament, name='JoinTournament'),
    path('tournament/<int:tournament_id>/start/', views.start_tournament, name='StartTournament'),
    path('tournament/<int:tournament_id>/leave/', views.leave_tournament, name='LeaveTournament'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
