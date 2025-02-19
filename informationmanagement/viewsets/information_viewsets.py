from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import Information
from ..serializers.information_serializers import (
    InformationListSerializers, InformationRetrieveSerializers, InformationWriteSerializers
)
from ..utilities.filters import InformationFilter
from mainproj.permissions import DynamicModelPermission

class informationViewsets(viewsets.ModelViewSet):
    permission_classes = [DynamicModelPermission]
    # pagination_class = MyPageNumberPagination
    queryset = Information.objects.all().order_by('-id')
    filterset_class = InformationFilter
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # 🔹 FIX: Corrected Order
    search_fields = [
        'id', 'title', 'publish_date', 'active_period_start', 'active_period_end', 
        'sublevel__name', 'course__name', 'created_date', 'updated_date'
    ]
    ordering_fields = search_fields

    def get_serializer_class(self):
        """Return different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return InformationWriteSerializers
        elif self.action == 'retrieve':
            return InformationRetrieveSerializers
        return InformationListSerializers

    def create(self, request, *args, **kwargs):
        """
        Handles creating a new Information object.
        Returns the full object data using InformationRetrieveSerializers.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(InformationRetrieveSerializers(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Handles updating an existing Information object.
        Returns the updated object data using InformationRetrieveSerializers.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(InformationRetrieveSerializers(instance).data, status=status.HTTP_200_OK)

