from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Certification
from ..serializers.certification_serializers import CertificationListSerializers, CertificationRetrieveSerializers, CertificationWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class certificationViewsets(viewsets.ModelViewSet):
    serializer_class = CertificationListSerializers
    # permission_classes = [certificationPermission]
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Certification.objects.all().order_by('-id')
# ('name', 'is_show', 'image', 'created_date', 'created_date_time', 'updated_date', )
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'is_show','created_date']
    ordering_fields = ['id','name', 'is_show']

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
            return CertificationWriteSerializers
        elif self.action == 'retrieve':
            return CertificationRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

