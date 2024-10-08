from django.urls import path, include
from .viewsets.login import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('gettoken/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('refresh-token',TokenRefreshView.as_view(),name = 'refresh-token'),
    path('token-verify/',TokenVerifyView.as_view(),name="token_verify"),
]