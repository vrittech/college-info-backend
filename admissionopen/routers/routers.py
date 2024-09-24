from rest_framework.routers import DefaultRouter
from ..viewsets.admissionopen_viewsets import admissionopenViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('admissionopen', admissionopenViewsets, basename="admissionopenViewsets")
