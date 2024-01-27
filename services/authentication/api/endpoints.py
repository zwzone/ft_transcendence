from django.urls import path
from . import views

urlpatterns = [
    path('intra/', views.intra_auth, name='intraView'),
    path('intra/callback/', views.intra_callback_auth, name='intracallbackView'),
    path('google/', views.google_auth, name='googleView'),
    path('google/callback/', views.google_callback_auth, name='googlecallbackView'),
    path('isloggedin/', views.is_logged_in_auth, name='isloggedinView'),
    path('logout/', views.logout_user, name='logoutView'),
    path('2FA/submit/', views.submit_two_factor, name='submit_two_factorView')
]
