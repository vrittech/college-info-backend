from rest_framework.routers import DefaultRouter
from ..viewsets.preparationinquiries_viewsets import preparationinquiriesViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('preparationinquiries', preparationinquiriesViewsets, basename="preparationinquiriesViewsets")
