from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import EventGallery
from ..serializers.eventgallery_serializers import EventGalleryListSerializers, EventGalleryRetrieveSerializers, EventGalleryWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from ..models import Event

class eventgalleryViewsets(viewsets.ModelViewSet):
    serializer_class = EventGalleryListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = EventGallery.objects.all().order_by('-position')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'event': ['exact'],
        'is_featured_image': ['exact'],
        'created_date': ['exact', 'lte', 'gte'],
        'updated_date': ['exact', 'lte', 'gte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-position')
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventGalleryWriteSerializers
        elif self.action == 'retrieve':
            return EventGalleryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    @action(detail=False, methods=['get'],permission_classes=[AllowAny], url_path="latest-images/(?P<event_slug>[^/]+)")
    def latest_college_images(self, request, event_slug=None, *args, **kwargs):
        # Fetch the college using slug
        event = get_object_or_404(Event, slug=event_slug)

        # Get the latest 5 images of the specified college
        images = EventGallery.objects.filter(event=event).order_by('-created_date')[:5]

        # Serialize and return the data
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    

