from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('intra/', views.intra_auth, name='intraView'),
    path('intra/callback/', views.intra_callback_auth, name='intracallbackView'),
    path('google/', views.google_auth, name='googleView'),
    path('google/callback/', views.google_callback_auth, name='googlecallbackView'),
    path('logout/', views.logout_user, name='logoutView'),
    path('2FA/qrcode/', views.qrcode_two_factor, name='qrcode_two_factorView'),
    path('2FA/verify/', views.verify_two_factor, name='verify_two_factorView'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
