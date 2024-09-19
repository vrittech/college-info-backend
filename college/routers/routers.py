from rest_framework.routers import DefaultRouter
from ..viewsets.college_viewsets import collegeViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('college', collegeViewsets, basename="collegeViewsets")
