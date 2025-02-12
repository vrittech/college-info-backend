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
from collections import defaultdict, OrderedDict

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
        Group permissions by models only, replacing codename with action labels.
        Sorted by model name in ascending order.
        """
        permissions = self.get_queryset()
        grouped_permissions = defaultdict(list)

        # Standard and custom action mappings
        ACTION_MAPPING = {
            "add": "Add",
            "change": "Edit",
            "delete": "Delete",
            "view": "View",
            "manage": "Manage",
            "verify": "Verify"
        }

        for permission in permissions:
            model_name = permission.content_type.model
            codename_parts = permission.codename.split("_")  

            # Extract action key
            action_key = codename_parts[0] if len(codename_parts) > 1 else permission.codename  

            # Map action name or default to capitalized version
            action_label = ACTION_MAPPING.get(action_key, action_key.capitalize())

            # Clean "Can" from permission name
            clean_name = permission.name.replace("Can ", "")

            grouped_permissions[model_name].append({
                'id': permission.id,
                'name': clean_name,
                'action': action_label
            })

        # Sort model names alphabetically
        sorted_permissions = OrderedDict(sorted(grouped_permissions.items()))

        return Response(sorted_permissions)
