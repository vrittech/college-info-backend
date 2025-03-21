from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Level
from ..serializers.level_serializers import LevelListSerializers, LevelRetrieveSerializers, LevelWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class levelViewsets(viewsets.ModelViewSet):
    serializer_class = LevelListSerializers
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Level.objects.all().order_by('-id')
# ('sublevel', 'name', 'description', 'image', 'created_date', 'created_date_time', )
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','sublevel__name', 'name', 'description', 'created_date', 'created_date_time',]
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'sublevel': ['exact'],
        'name': ['exact'],
        'is_show': ['exact'],
        'created_date': ['exact', 'lte', 'gte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LevelWriteSerializers
        elif self.action == 'retrieve':
            return LevelRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

