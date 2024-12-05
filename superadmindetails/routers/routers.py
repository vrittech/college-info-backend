from rest_framework.routers import DefaultRouter
from ..viewsets.superadmindetails_viewsets import superadmindetailsViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('superadmindetails', superadmindetailsViewsets, basename="superadmindetailsViewsets")
