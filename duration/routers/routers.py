from rest_framework.routers import DefaultRouter
from ..viewsets.duration_viewsets import durationViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('duration', durationViewsets, basename="durationViewsets")
