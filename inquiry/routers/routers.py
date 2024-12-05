from rest_framework.routers import DefaultRouter
from ..viewsets.inquiry_viewsets import inquiryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('inquiry', inquiryViewsets, basename="inquiryViewsets")
