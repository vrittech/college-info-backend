from rest_framework.routers import DefaultRouter
from ..viewsets.socialmedia_viewsets import socialmediaViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('socialmedia', socialmediaViewsets, basename="socialmediaViewsets")
