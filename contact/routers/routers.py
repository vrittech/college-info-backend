from rest_framework.routers import DefaultRouter
from ..viewsets.contact_viewsets import contactViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('contact', contactViewsets, basename="contactViewsets")
