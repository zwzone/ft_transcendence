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
    path('intracallback/', intra_callback_auth, name='intracallbackView'),
    path('google/', google_auth, name='googleView'),
    path('googlecallback/', google_callback_auth, name='googlecallbackView'),
    path('islogedin/', is_logged_in_auth, name='islogedinView'),
    path('logout/', logout_user, name='logoutView'),
]
