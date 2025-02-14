from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import EventOrganizer
from ..serializers.eventorganizer_serializers import EventOrganizerListSerializers, EventOrganizerRetrieveSerializers, EventOrganizerWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class eventorganizerViewsets(viewsets.ModelViewSet):
    serializer_class = EventOrganizerListSerializers
    permission_classes = [DynamicModelPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = EventOrganizer.objects.all().order_by('-id')

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
            return EventOrganizerWriteSerializers
        elif self.action == 'retrieve':
            return EventOrganizerRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

