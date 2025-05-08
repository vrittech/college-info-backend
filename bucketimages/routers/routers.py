from rest_framework.routers import DefaultRouter
from ..viewsets.bucketfile_viewsets import bucketfileViewsets
# from ..viewsets.bucketsynclog_viewsets import bucketsynclogViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('bucket-file', bucketfileViewsets, basename="bucketfileViewsets")
# router.register('bucketsynclog', bucketsynclogViewsets, basename="bucketsynclogViewsets")
