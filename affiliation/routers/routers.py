from rest_framework.routers import DefaultRouter
from ..viewsets.affiliation_viewsets import affiliationViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('affiliation', affiliationViewsets, basename="affiliationViewsets")
