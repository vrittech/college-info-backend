from rest_framework.routers import DefaultRouter
from ..viewsets.facility_viewsets import facilityViewsets
from ..viewsets.collegefacility_viewsets import collegefacilityViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('facility', facilityViewsets, basename="facilityViewsets")
router.register('collegefacility', collegefacilityViewsets, basename="collegefacilityViewsets")
