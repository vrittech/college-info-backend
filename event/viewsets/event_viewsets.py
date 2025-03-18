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
from ..utilities.permissions import eventPermission
from mainproj.permissions import DynamicModelPermission
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
import requests


class eventViewsets(viewsets.ModelViewSet):
    serializer_class = EventListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Event.objects.all().order_by('-id')
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id', 'event_name', 'venue', 'category__name', 'organizer__name']  # Fields to search
    ordering_fields = ['id', 'event_name', 'start_date', 'end_date', 'is_featured_event']  # Fields to sort
    ordering = ['-id']  # Default ordering
    filterset_class = EventFilter
    
    def get_object(self):
        """
        Override get_object to allow lookup by either 'id' or 'slug'.
        """
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)  # Get lookup value from URL
        if lookup_value.isdigit():  # Check if lookup_value is numeric (ID)
            return get_object_or_404(queryset, id=int(lookup_value))
        return get_object_or_404(queryset, slug=lookup_value)  # Otherwise, lookup by slug

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

        return self.get_formatted_response(event_instance,status.HTTP_201_CREATED,request)

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

        return self.get_formatted_response(event_instance,status.HTTP_200_OK,request)

    def get_formatted_response(self, event_instance, status, request):
        """Formats the response to match the expected structure."""
        response_data = {
            "public_id": str(event_instance.public_id),
            "slug": event_instance.slug,
            "event_name": event_instance.event_name,
            "start_date": event_instance.start_date,
            "end_date": event_instance.end_date,
            "duration": event_instance.duration,
            "duration_type": event_instance.duration_type,
            "event_type": event_instance.event_type,
            "venue": event_instance.venue,
            "online_platform": event_instance.online_platform,
            "online_seat_limit": event_instance.online_seat_limit,
            "offline_seat_limit": event_instance.offline_seat_limit,
            "is_offline_seat_limit": event_instance.is_offline_seat_limit,
            "is_online_seat_limit": event_instance.is_online_seat_limit,
            "is_registration": event_instance.is_registration,
            "registration_link": event_instance.registration_link,
            "registration_type": event_instance.registration_type,
            "amount": str(event_instance.amount) if event_instance.amount else None,
            "amount_type": event_instance.amount_type,
            "amount_country": event_instance.amount_country,
            "description": event_instance.description,
            "is_featured_event": event_instance.is_featured_event,
            "featured_image": event_instance.featured_image,
            "category": EventCategoryRetrieveSerializers(event_instance.category.all(), many=True).data,
            "organizer": EventOrganizerRetrieveSerializers(event_instance.organizer.all(), many=True).data,
            "created_date_time": event_instance.created_date_time,
            "created_date": event_instance.created_date,
            "updated_date": event_instance.updated_date,
            "image": [
                {"id": img.id, "image": img.image.url}
                for img in event_instance.image.all()
            ],
        }

        return Response(response_data, status=status)


    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

