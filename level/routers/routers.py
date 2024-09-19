from rest_framework.routers import DefaultRouter
from ..viewsets.level_viewsets import levelViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('level', levelViewsets, basename="levelViewsets")
