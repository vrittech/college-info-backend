from rest_framework.routers import DefaultRouter
from ..viewsets.collegeleveltype_viewsets import collegeleveltypeViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('collegeleveltype', collegeleveltypeViewsets, basename="collegeleveltypeViewsets")
