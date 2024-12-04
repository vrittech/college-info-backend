from rest_framework.routers import DefaultRouter
from ..viewsets.eventorganizer_viewsets import eventorganizerViewsets
# from ..viewsets.image_viewsets import imageViewsets
from ..viewsets.event_viewsets import eventViewsets
from ..viewsets.eventcategory_viewsets import eventcategoryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('eventorganizer', eventorganizerViewsets, basename="eventorganizerViewsets")
router.register('eventcategory', eventcategoryViewsets, basename="eventcategoryViewsets")
router.register('event', eventViewsets, basename="eventViewsets")
# router.register('image', imageViewsets, basename="imageViewsets")
