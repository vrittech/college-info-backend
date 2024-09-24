from rest_framework.routers import DefaultRouter
from ..viewsets.facility_viewsets import facilityViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('facility', facilityViewsets, basename="facilityViewsets")
