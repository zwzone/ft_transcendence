from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/last-matches/', LastMatchesView.as_view(), name='lastMatches'),
]
