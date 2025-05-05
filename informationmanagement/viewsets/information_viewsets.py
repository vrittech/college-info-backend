from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import Information
from ..serializers.information_serializers import (
    InformationListSerializers, InformationRetrieveSerializers, InformationWriteSerializers
)
from ..utilities.filters import InformationFilter
from ..utilities.pagination import MyPageNumberPagination
from mainproj.permissions import DynamicModelPermission
from django.shortcuts import get_object_or_404


from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

cache_time = 1800  # 15 minutes


class informationViewsets(viewsets.ModelViewSet):
    permission_classes = [DynamicModelPermission]
    pagination_class = MyPageNumberPagination
    queryset = Information.objects.all().order_by('-id')
    filterset_class = InformationFilter
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # 🔹 FIX: Corrected Order
    search_fields = [
        'id', 'title', 'publish_date', 'active_period_start', 'active_period_end', 
        'sublevel__name', 'course__name', 'created_date', 'updated_date'
    ]
    ordering_fields = search_fields
    
    def get_object(self):
        """
        Override get_object to allow lookup by either 'id' or 'slug'.
        """
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)  # Get lookup value from URL
        if lookup_value.isdigit():  # Check if lookup_value is numeric (ID)
            return get_object_or_404(queryset, id=int(lookup_value))
        return get_object_or_404(queryset, slug=lookup_value)  # Otherwise, lookup by slug
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        """Return different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return InformationWriteSerializers
        elif self.action == 'retrieve':
            return InformationRetrieveSerializers
        return InformationListSerializers

    # List action caching
    def _list(self, request, *args, **kwargs):
        """Actual list implementation"""
        print("Information List - uncached version")
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="InformationList"))
    def _cached_list(self, request, *args, **kwargs):
        """Cached version of list"""
        return self._list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_list(request, *args, **kwargs)
        return self._list(request, *args, **kwargs)

    # Retrieve action caching
    def _retrieve(self, request, *args, **kwargs):
        """Actual retrieve implementation"""
        print("Information Retrieve - uncached version")
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="InformationRetrieve"))
    def _cached_retrieve(self, request, *args, **kwargs):
        """Cached version of retrieve"""
        return self._retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_retrieve(request, *args, **kwargs)
        return self._retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create with retrieve serializer response"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(InformationRetrieveSerializers(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update with retrieve serializer response"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(InformationRetrieveSerializers(instance).data, status=status.HTTP_200_OK)