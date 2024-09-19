from rest_framework.routers import DefaultRouter
from ..viewsets.emailsetup_viewsets import emailsetupViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('emailsetup', emailsetupViewsets, basename="emailsetupViewsets")
