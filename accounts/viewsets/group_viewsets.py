from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers.group_serializers import GroupSerializer
from ..utilities.pagination import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..utilities.groupfilter import GroupFilter
from rest_framework.exceptions import PermissionDenied
from accounts.models import CustomUser as User


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
        related_models = []

        # Check if any user is assigned to this group
        if User.objects.filter(groups=instance).exists():
            related_models.append(f"{User._meta.app_label}.{User.__name__}")

        # Optionally check other models if you still want
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if isinstance(field, (ForeignKey, ManyToManyField)) and field.related_model == Group:
                    filter_kwargs = {f"{field.name}": instance}
                    if model.objects.filter(**filter_kwargs).exists():
                        model_label = f"{model._meta.app_label}.{model.__name__}"
                        if model_label not in related_models:
                            related_models.append(model_label)

        if related_models:
            return Response(
                {
                    "detail": "This group is being used in the following models. "
                            "Please update/remove those references before deletion.",
                    "used_in_models": related_models
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