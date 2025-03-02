from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Advertisement
from ..serializers.advertisement_serializers import AdvertisementListSerializers, AdvertisementRetrieveSerializers, AdvertisementWriteSerializers
from ..utilities.importbase import *
from ..utilities.permissions import advertisementPermission
from mainproj.permissions import DynamicModelPermission

class advertisementViewsets(viewsets.ModelViewSet):
    serializer_class = AdvertisementListSerializers
    # permission_classes = [advertisementPermission]
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Advertisement.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'link','placement', 'created_date', 'updated_date']
    ordering_fields = ['id','name', 'link','placement', 'created_date', 'updated_date']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'placement': ['exact'],
        'created_date': ['exact','gte','lte'],
        'updated_date': ['exact','gte','lte'],
    }
# ('name', 'link', 'image', 'placement', 'created_date', 'updated_date', )
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AdvertisementWriteSerializers
        elif self.action == 'retrieve':
            return AdvertisementRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

