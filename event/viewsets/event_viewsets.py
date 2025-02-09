from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Event
from ..serializers.event_serializers import EventListSerializers, EventRetrieveSerializers, EventWriteSerializers
from ..serializers.eventcategory_serializers import EventCategoryRetrieveSerializers
from ..serializers.eventorganizer_serializers import EventOrganizerRetrieveSerializers
from ..utilities.filter import EventFilter
from ..utilities.pagination import MyPageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

class eventViewsets(viewsets.ModelViewSet):
    serializer_class = EventListSerializers
    # permission_classes = [eventPermission]
    authentication_classes = [JWTAuthentication]
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_instance = serializer.save()

        return self.get_formatted_response(event_instance,status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Handles PUT (full update) and PATCH (partial update).
        Ensures that new images and Many-to-Many relationships are updated correctly.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        event_instance = serializer.save()

        return self.get_formatted_response(event_instance,status.HTTP_200_OK)

    def get_formatted_response(self, event_instance, status):
        """Formats the response to match the expected structure."""
        response_data = {
            "category": EventCategoryRetrieveSerializers(event_instance.category.all(), many=True).data,
            "organizer": EventOrganizerRetrieveSerializers(event_instance.organizer.all(), many=True).data,
            "event_name": event_instance.event_name,
            "duration": event_instance.duration,
            "event_type": event_instance.event_type,
            "slug": event_instance.slug,
            "venue": event_instance.venue,
            "offline_seat_limit": event_instance.offline_seat_limit,
            "is_registration": event_instance.is_registration,
            "registration_link": event_instance.registration_link,
            "registration_type": event_instance.registration_type,
            "amount": event_instance.amount,
            "amount_country": event_instance.amount_country,
            "description": event_instance.description,
            "start_date": event_instance.start_date,
            "end_date": event_instance.end_date,
            "images": [
                {"id": img.id, "image_url": img.image.url} for img in event_instance.image.all()
            ],
        }

        return Response(response_data, status= status)


    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

