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
    queryset = Event.objects.all().order_by('start_date')
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id', 'event_name', 'venue', 'category__name', 'organizer__name']  # Fields to search
    ordering_fields = ['id', 'event_name', 'start_date', 'end_date', 'is_featured_event']  # Fields to sort
    ordering = ['is_expired', 'start_date']
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

        # Use the retrieve serializer for response formatting
        response_serializer = EventRetrieveSerializers(event_instance, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

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

        # Use the retrieve serializer for response formatting
        response_serializer = EventRetrieveSerializers(event_instance, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

