from rest_framework.routers import DefaultRouter
from ..viewsets.collegetype_viewsets import collegetypeViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('collegetype', collegetypeViewsets, basename="collegetypeViewsets")
