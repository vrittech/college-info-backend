from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import SuperAdminDetails
from ..serializers.superadmindetails_serializers import SuperAdminDetailsListSerializers, SuperAdminDetailsRetrieveSerializers, SuperAdminDetailsWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class superadmindetailsViewsets(viewsets.ModelViewSet):
    serializer_class = SuperAdminDetailsListSerializers
    permission_classes = [superadmindetailsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = SuperAdminDetails.objects.all().order_by('-id')
# ('name', 'email', 'phone_number', 'location', 'social_media_links', 'created_at', 'updated_at', )
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'email', 'phone_number', 'location', 'social_media_links', 'created_at', 'updated_at']
    ordering_fields = ['id','name', 'phone_number', 'location', 'social_media_links', 'created_at', 'updated_at']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'location': ['exact'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SuperAdminDetailsWriteSerializers
        elif self.action == 'retrieve':
            return SuperAdminDetailsRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

