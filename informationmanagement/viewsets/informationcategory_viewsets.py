from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import InformationCategory
from ..serializers.informationcategory_serializers import InformationCategoryListSerializers, InformationCategoryRetrieveSerializers, InformationCategoryWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission
from ..utilities.pagination import MyPageNumberPagination
from django.shortcuts import get_object_or_404

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

cache_time = 1800  # 15 minutes


class informationcategoryViewsets(viewsets.ModelViewSet):
    serializer_class = InformationCategoryListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = InformationCategory.objects.all().order_by('-id')
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'is_show', 'created_date', 'updated_date']
    ordering_fields = ['id','name', 'is_show', 'created_date', 'updated_date']
# ('name', 'is_show', 'image', 'created_date', 'updated_date', )

    def get_object(self):
        """
        Override get_object to allow lookup by either 'id' or 'slug'.
        """
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)  # Get lookup value from URL
        if lookup_value.isdigit():  # Check if lookup_value is numeric (ID)
            return get_object_or_404(queryset, id=int(lookup_value))
        return get_object_or_404(queryset, slug=lookup_value)  # Otherwise, lookup by slug
   
    filterset_fields = {
        'is_show': ['exact'],
        'slug': ['exact'],
        'id': ['exact'],
        'name': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InformationCategoryWriteSerializers
        elif self.action == 'retrieve':
            return InformationCategoryRetrieveSerializers
        return super().get_serializer_class()
    
    # List action caching
    def _list(self, request, *args, **kwargs):
        """Actual list implementation"""
        print("InformationCategory List - uncached version")
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="InformationCategoryList"))
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
        print("InformationCategory Retrieve - uncached version")
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="InformationCategoryRetrieve"))
    def _cached_retrieve(self, request, *args, **kwargs):
        """Cached version of retrieve"""
        return self._retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_retrieve(request, *args, **kwargs)
        return self._retrieve(request, *args, **kwargs)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

