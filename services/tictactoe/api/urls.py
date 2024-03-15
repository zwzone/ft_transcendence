from    django.urls import  path
from . import settings
from django.conf.urls.static import static

print( settings.STATIC_URL, flush=True)

urlpatterns = [
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
