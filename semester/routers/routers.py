from rest_framework.routers import DefaultRouter
from ..viewsets.semester_viewsets import semesterViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('semester', semesterViewsets, basename="semesterViewsets")
