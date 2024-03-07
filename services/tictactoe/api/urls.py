from    django.urls import  path
from    .           import  views
from . import settings
from django.conf.urls.static import static

print( settings.STATIC_URL, flush=True)

urlpatterns = [
    path( 'match/', views.play)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
