from rest_framework.routers import DefaultRouter
from ..viewsets.course_viewsets import courseViewsets
from ..viewsets.coursecurriculumfile_viewsets import coursecurriculumfileViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('course', courseViewsets, basename="courseViewsets")
router.register('coursecurriculumfile', coursecurriculumfileViewsets, basename="coursecurriculumfileViewsets")
