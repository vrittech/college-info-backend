from rest_framework.routers import DefaultRouter
from ..viewsets.placementposition_viewsets import placementpositionViewsets
from ..viewsets.advertisement_viewsets import advertisementViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('placementposition', placementpositionViewsets, basename="placementpositionViewsets")
router.register('advertisement', advertisementViewsets, basename="advertisementViewsets")
