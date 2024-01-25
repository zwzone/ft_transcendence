from django.urls import path
from .views import (
    intra_auth,
    intra_callback_auth,
    google_auth,
    google_callback_auth,
    is_logged_in_auth,
    logout_user
)

urlpatterns = [
    path('intra/', intra_auth, name='intraView'),
    path('intra/callback/', intra_callback_auth, name='intracallbackView'),
    path('google/', google_auth, name='googleView'),
    path('google/callback/', google_callback_auth, name='googlecallbackView'),
    path('isloggedin/', is_logged_in_auth, name='isloggedinView'),
    path('logout/', logout_user, name='logoutView'),
    path('submit-2FAauth/', logout_user, name='')
]
