from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import email_setup_viewsets

router = DefaultRouter()

router.register('email-setup', email_setup_viewsets.EmailSetupViewset, basename="EmailSetupViewset")

urlpatterns = [    
    # path('', include(router.urls)),
]