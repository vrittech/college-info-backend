from rest_framework.routers import DefaultRouter
from ..viewsets.popup_viewsets import popupViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('popup', popupViewsets, basename="popupViewsets")
