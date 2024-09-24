from rest_framework.routers import DefaultRouter
from ..viewsets.coursesandfees_viewsets import coursesandfeesViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('coursesandfees', coursesandfeesViewsets, basename="coursesandfeesViewsets")
