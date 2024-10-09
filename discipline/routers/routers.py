from rest_framework.routers import DefaultRouter
from ..viewsets.discipline_viewsets import disciplineViewsets

router = DefaultRouter()


router.register('discipline', disciplineViewsets, basename="disciplineViewsets")
