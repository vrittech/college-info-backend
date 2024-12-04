from rest_framework.routers import DefaultRouter
# from ..viewsets.year_viewsets import yearViewsets
from ..viewsets.information_viewsets import informationViewsets
from ..viewsets.informationcategory_viewsets import informationcategoryViewsets
from ..viewsets.informationtagging_viewsets import informationtaggingViewsets

router = DefaultRouter()


# router.register('year', yearViewsets, basename="yearViewsets")
router.register('informationtagging', informationtaggingViewsets, basename="informationtaggingViewsets")
router.register('informationcategory', informationcategoryViewsets, basename="informationcategoryViewsets")
router.register('information', informationViewsets, basename="informationViewsets")
