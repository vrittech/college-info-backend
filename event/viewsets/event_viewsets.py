from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Event
from ..serializers.event_serializers import EventListSerializers, EventRetrieveSerializers, EventWriteSerializers
from ..utilities.importbase import *
from ..utilities.filter import EventFilter

class eventViewsets(viewsets.ModelViewSet):
    serializer_class = EventListSerializers
    # permission_classes = [eventPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Event.objects.all().order_by('-id')
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id', 'event_name', 'venue', 'category__name', 'organizer__name']  # Fields to search
    ordering_fields = ['id', 'event_name', 'start_date', 'end_date', 'is_featured_event']  # Fields to sort
    ordering = ['-id']  # Default ordering
    filterset_class = EventFilter

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventWriteSerializers
        elif self.action == 'retrieve':
            return EventRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

