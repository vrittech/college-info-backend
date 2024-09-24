from rest_framework.routers import DefaultRouter
from ..viewsets.course_viewsets import courseViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('course', courseViewsets, basename="courseViewsets")
