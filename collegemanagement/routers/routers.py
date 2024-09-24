from rest_framework.routers import DefaultRouter
from ..viewsets.collegegallery_viewsets import collegegalleryViewsets
from ..viewsets.college_viewsets import collegeViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('collegegallery', collegegalleryViewsets, basename="collegegalleryViewsets")
router.register('college', collegeViewsets, basename="collegeViewsets")
