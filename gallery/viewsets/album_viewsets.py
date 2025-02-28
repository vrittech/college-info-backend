from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Album
from ..serializers.album_serializers import AlbumListSerializers, AlbumRetrieveSerializers, AlbumWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class albumViewsets(viewsets.ModelViewSet):
    serializer_class = AlbumListSerializers
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Album.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']

    filterset_fields = {
        
        'id': ['exact'],
        'created_date': ['exact', 'lte', 'gte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AlbumWriteSerializers
        elif self.action == 'retrieve':
            return AlbumRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

