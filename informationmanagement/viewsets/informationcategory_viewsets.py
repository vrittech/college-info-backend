from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import InformationCategory
from ..serializers.informationcategory_serializers import InformationCategoryListSerializers, InformationCategoryRetrieveSerializers, InformationCategoryWriteSerializers
from ..utilities.importbase import *

class informationcategoryViewsets(viewsets.ModelViewSet):
    serializer_class = InformationCategoryListSerializers
    # permission_classes = [informationmanagementPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = InformationCategory.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'is_show', 'created_date', 'updated_date']
    ordering_fields = ['id','name', 'is_show', 'created_date', 'updated_date']
# ('name', 'is_show', 'image', 'created_date', 'updated_date', )
   
    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InformationCategoryWriteSerializers
        elif self.action == 'retrieve':
            return InformationCategoryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

