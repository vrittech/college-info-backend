from rest_framework.routers import DefaultRouter
from ..viewsets.district_viewsets import districtViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('district', districtViewsets, basename="districtViewsets")
