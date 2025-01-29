from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeType
from ..serializers.collegetype_serializers import CollegeTypeListSerializers, CollegeTypeRetrieveSerializers, CollegeTypeWriteSerializers
from ..utilities.importbase import *

class collegetypeViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeTypeListSerializers
    # permission_classes = [collegetypePermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeType.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    filterset_fields = {
            'id': ['exact'],
            'name': ['exact'],
            'is_show': ['exact'],
            'created_date': ['exact', 'lte', 'gte'],
            'updated_date': ['exact', 'lte', 'gte'],
        }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeTypeWriteSerializers
        elif self.action == 'retrieve':
            return CollegeTypeRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

