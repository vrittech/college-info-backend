from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Affiliation
from ..serializers.affiliation_serializers import AffiliationListSerializers, AffiliationRetrieveSerializers, AffiliationWriteSerializers
from ..utilities.importbase import *

class affiliationViewsets(viewsets.ModelViewSet):
    serializer_class = AffiliationListSerializers
    # permission_classes = [affiliationPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Affiliation.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name','district','address']
    ordering_fields = ['id','name','district','address','created_date','updated_date']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'address': ['exact'],
        'district': ['exact'],
        'university_type': ['exact'],
        'certification': ['exact'],
        'created_date': ['exact','gte','lte'],
        'established_year': ['exact','gte','lte'],
        'updated_date': ['exact','gte','lte'],
    }
# ('name', 'established_year', '.year,validators', 'google_map_embed_url', 'latitude', 'longitude', 'address', 'district', 'university_type', 'certification', 'phone_number', 'email', 'description', 'logo_image', 'cover_image', 'created_date', 'updated_date', )
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AffiliationWriteSerializers
        elif self.action == 'retrieve':
            return AffiliationRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

