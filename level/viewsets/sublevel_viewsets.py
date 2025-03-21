from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import SubLevel
from ..serializers.sublevel_serializers import SubLevelListSerializers, SubLevelRetrieveSerializers, SubLevelWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission


class sublevelViewsets(viewsets.ModelViewSet):
    serializer_class = SubLevelListSerializers
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = SubLevel.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'created_date',]
    ordering_fields = ['id']

    filterset_fields = {
            'id': ['exact'],
            'name': ['exact'],
            'is_show': ['exact'],
            'created_date': ['exact', 'lte', 'gte'],
        }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SubLevelWriteSerializers
        elif self.action == 'retrieve':
            return SubLevelRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

