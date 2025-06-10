from rest_framework.routers import DefaultRouter
from ..viewsets.file_viewsets import fileViewsets
from ..viewsets.result_viewsets import resultViewsets

router = DefaultRouter()


router.register('resultfile', fileViewsets, basename="fileViewsets")
router.register('result', resultViewsets, basename="resultViewsets")
