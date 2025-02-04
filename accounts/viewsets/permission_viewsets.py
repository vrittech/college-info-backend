from django.apps import apps
from django.contrib.auth.models import Permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from collections import defaultdict
from ..utilities.pagination import MyPageNumberPagination
from ..serializers.permission_serializers import PermissionSerializer


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list permissions and provide an additional grouped-by-apps view.
    """
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['codename', 'id', 'name']
    filterset_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'codename': ['exact', 'icontains']
    }
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        """
        Dynamically fetch permissions for custom apps.
        """
        # Define excluded apps (Django built-in and third-party)
        excluded_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'corsheaders',
            'rest_framework',
            'drf_yasg',
            'django_celery_beat',
            'django_filters',
        ]

        # Dynamically identify custom app labels
        custom_app_labels = [
            app.label for app in apps.get_app_configs()
            if app.name not in excluded_apps
        ]

        # Fetch permissions related to these custom apps
        return Permission.objects.filter(
            content_type__app_label__in=custom_app_labels
        ).select_related('content_type')

    @action(detail=False, methods=['get'])
    def grouped_by_model(self, request):
        """
        Group permissions by models only.
        """
        # Fetch permissions and group by model
        permissions = self.get_queryset()
        grouped_permissions = defaultdict(list)

        for permission in permissions:
            model_name = permission.content_type.model
            grouped_permissions[model_name].append({
                'id': permission.id,
                'name': permission.name,
                'codename': permission.codename,
            })

        # Convert grouped data to a serializable dict
        return Response(dict(grouped_permissions))