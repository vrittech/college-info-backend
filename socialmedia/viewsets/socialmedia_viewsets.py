from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import SocialMedia
from ..serializers.socialmedia_serializers import SocialMediaListSerializers, SocialMediaRetrieveSerializers, SocialMediaWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class socialmediaViewsets(viewsets.ModelViewSet):
    serializer_class = SocialMediaListSerializers
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = SocialMedia.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
    }
# ('name', 'link', 'icon=models.ImageField(upload_to='components/banner',null', 'created_date', 'updated_date', )
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SocialMediaWriteSerializers
        elif self.action == 'retrieve':
            return SocialMediaRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

