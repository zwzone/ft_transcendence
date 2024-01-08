from django.urls import path

from authenticationapp.views import IntraAuthAPIView ,IntraRedirectAPIView

urlpatterns = [
    path('auth/', IntraAuthAPIView.as_view(), name='authAPI'),
    path('redirect/', IntraRedirectAPIView.as_view(), name='redirectAPI'),
]