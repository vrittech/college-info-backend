from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Facility
from ..serializers.facility_serializers import FacilityListSerializers, FacilityRetrieveSerializers, FacilityWriteSerializers
from ..utilities.importbase import *

class facilityViewsets(viewsets.ModelViewSet):
    serializer_class = FacilityListSerializers
    # permission_classes = [facilitiesPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Facility.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'is_show': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FacilityWriteSerializers
        elif self.action == 'retrieve':
            return FacilityRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

