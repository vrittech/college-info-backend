from rest_framework.routers import DefaultRouter
from ..viewsets.level_viewsets import levelViewsets
from ..viewsets.sublevel_viewsets import sublevelViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('level', levelViewsets, basename="levelViewsets")
router.register('sublevel', sublevelViewsets, basename="sublevelViewsets")
