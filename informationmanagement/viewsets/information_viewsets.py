from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Information
from ..serializers.information_serializers import InformationListSerializers, InformationRetrieveSerializers, InformationWriteSerializers
from ..utilities.importbase import *
from ..utilities.filters import InformationFilter
from rest_framework import viewsets, status
from rest_framework.response import Response

class informationViewsets(viewsets.ModelViewSet):
    serializer_class = InformationListSerializers
    # permission_classes = [informationmanagementPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Information.objects.all().order_by('-id')
    filterset_class = InformationFilter
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','title', 'publish_date', 'active_period_start', 'active_period_end', 'sublevel__name', 'course__name','created_date', 'updated_date',]
    ordering_fields =  ['id','title', 'publish_date', 'active_period_start', 'active_period_end', 'sublevel__name', 'course__name','created_date', 'updated_date',]

    # filterset_fields = {
    # 'id': ['exact'],
    # 'state': ['exact'],
    # 'title': ['exact', 'icontains'],
    # 'publish_date': ['exact', 'gte', 'lte'],
    # 'active_period_start': ['exact', 'gte', 'lte'],
    # 'active_period_end': ['exact', 'gte', 'lte'],
    # # 'level__name': ['exact', 'icontains'],
    # 'sublevel__name': ['exact', 'icontains'],
    # 'course__name': ['exact', 'icontains'],
    # 'created_date': ['exact', 'gte', 'lte'],
    # 'updated_date': ['exact', 'gte', 'lte'],
    # }

# ('title', 'publish_date', 'active_period_start', 'active_period_end', 'level', 'sublevel', 'course', 'affiliation', 'district', 'college', 'faculty', 'information_tagging', 'information_category', 'short_description', 'description', 'image', 'file', 'is_view', 'created_date', 'updated_date', )
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InformationWriteSerializers
        elif self.action == 'retrieve':
            return InformationRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    def get_serializer_class(self):
            """
            Returns the appropriate serializer class based on the request type.
            """
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

    def get_queryset(self):
        """
        Allows additional filtering logic if needed.
        """
        queryset = super().get_queryset()
        return queryset