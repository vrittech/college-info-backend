from rest_framework.routers import DefaultRouter
from ..viewsets.custom_user_viewsets import CustomUserViewSet
from ..viewsets.group_viewsets import GroupViewSet
from ..viewsets.permission_viewsets import PermissionViewSet

router = DefaultRouter()
auto_api_routers = router

router.register('user', CustomUserViewSet, basename="CustomUser")
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)




