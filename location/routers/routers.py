from rest_framework.routers import DefaultRouter
from ..viewsets.location_viewsets import locationViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('location', locationViewsets, basename="locationViewsets")
