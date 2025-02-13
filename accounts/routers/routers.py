from rest_framework.routers import DefaultRouter
from ..viewsets.custom_user_viewsets import CustomUserViewSet
# from ..viewsets.groupextension_viewsets import groupextensionViewsets
# from ..viewsets.customuser_viewsets import customuserViewsets
from ..viewsets.group_viewsets import GroupViewSet
from ..viewsets.permission_viewsets import PermissionViewSet

router = DefaultRouter()
auto_api_routers = router

router.register('user', CustomUserViewSet, basename="CustomUser")
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'permissions', PermissionViewSet, basename='permission')




# router.register('customuser', customuserViewsets, basename="customuserViewsets")
# router.register('groupextension', groupextensionViewsets, basename="groupextensionViewsets")
