from rest_framework.routers import DefaultRouter
from ..viewsets.socialmedia_viewsets import socialmediaViewsets
from ..viewsets.collegesocialmedia_viewsets import collegesocialmediaViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('socialmedia', socialmediaViewsets, basename="socialmediaViewsets")
router.register('collegesocialmedia', collegesocialmediaViewsets, basename="collegesocialmediaViewsets")
