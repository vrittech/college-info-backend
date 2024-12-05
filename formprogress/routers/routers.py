from rest_framework.routers import DefaultRouter
from ..viewsets.formstepprogress_viewsets import formstepprogressViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('formstepprogress', formstepprogressViewsets, basename="formstepprogressViewsets")
