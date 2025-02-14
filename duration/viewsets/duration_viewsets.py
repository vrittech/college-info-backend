from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Duration
from ..serializers.duration_serializers import DurationListSerializers, DurationRetrieveSerializers, DurationWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class durationViewsets(viewsets.ModelViewSet):
    serializer_class = DurationListSerializers
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Duration.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'created_date': ['exact', 'gte', 'lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DurationWriteSerializers
        elif self.action == 'retrieve':
            return DurationRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

