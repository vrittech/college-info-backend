from rest_framework.routers import DefaultRouter
from ..viewsets.collegeandcourseinquiries_viewsets import collegeandcourseinquiriesViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('collegeandcourseinquiries', collegeandcourseinquiriesViewsets, basename="collegeandcourseinquiriesViewsets")
