from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers.group_serializers import GroupSerializer
from ..utilities.pagination import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..utilities.groupfilter import GroupFilter
from rest_framework.exceptions import PermissionDenied
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework import status


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']
    filterset_class = GroupFilter
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.is_staff:
            return super().get_queryset()
        elif self.request.user.is_authenticated:
            return super().get_queryset().filter(id=self.request.user.id)
        else:
            return Group.objects.none()
    


    @staticmethod
    def perform_protection_check(instance):
        if instance.name.lower() == "college admin":
            raise PermissionDenied("You are not allowed to perform any action on the 'College Admin' group.")

    def get_object(self):
        instance = super().get_object()
        self.perform_protection_check(instance)
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Find users assigned to this group
        assigned_users = CustomUser.objects.filter(groups=instance)

        if assigned_users.exists():
            user_list = assigned_users.values_list('id', 'first_name', 'last_name', 'email')
            user_details = [
                f"{first_name} {last_name} <{email}>" if first_name or last_name else f"User ID {user_id} <{email}>"
                for user_id, first_name, last_name, email in user_list
            ]

            return Response(
                {
                    "detail": f"❌ Cannot delete this group because it is currently assigned to {assigned_users.count()} user(s).",
                    "message": "Please remove this group from the following users before attempting deletion.",
                    "affected_users": user_details
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.get_object()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.get_object()
        return super().partial_update(request, *args, **kwargs)