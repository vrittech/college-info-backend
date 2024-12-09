from rest_framework.routers import DefaultRouter
from ..viewsets.requestsubmission_viewsets import requestsubmissionViewsets

router = DefaultRouter()


router.register('requestsubmission', requestsubmissionViewsets, basename="requestsubmissionViewsets")
