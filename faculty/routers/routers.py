from rest_framework.routers import DefaultRouter
from ..viewsets.faculty_viewsets import facultyViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('faculty', facultyViewsets, basename="facultyViewsets")
