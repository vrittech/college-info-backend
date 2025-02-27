from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeFacility
from ..serializers.collegefacility_serializers import CollegeFacilityListSerializers, CollegeFacilityRetrieveSerializers, CollegeFacilityWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class collegefacilityViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeFacilityListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeFacility.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'college': ['exact'],
        'facility': ['exact'],
        'created_date': ['exact','gte','lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeFacilityWriteSerializers
        elif self.action == 'retrieve':
            return CollegeFacilityRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

