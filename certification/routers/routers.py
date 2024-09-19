from rest_framework.routers import DefaultRouter
from ..viewsets.certification_viewsets import certificationViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('certification', certificationViewsets, basename="certificationViewsets")
