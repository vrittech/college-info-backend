from rest_framework.routers import DefaultRouter
from ..viewsets.popup_viewsets import popupViewsets

router = DefaultRouter()


router.register('popup', popupViewsets, basename="popupViewsets")
