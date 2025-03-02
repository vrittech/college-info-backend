from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import PlacementPosition
from ..serializers.placementposition_serializers import PlacementPositionListSerializers, PlacementPositionRetrieveSerializers, PlacementPositionWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class placementpositionViewsets(viewsets.ModelViewSet):
    serializer_class = PlacementPositionListSerializers
    # permission_classes = [advertisementPermission]
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = PlacementPosition.objects.all().order_by('placement_name')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlacementPositionWriteSerializers
        elif self.action == 'retrieve':
            return PlacementPositionRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

