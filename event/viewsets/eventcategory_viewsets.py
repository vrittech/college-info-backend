from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import EventCategory
from ..serializers.eventcategory_serializers import EventCategoryListSerializers, EventCategoryRetrieveSerializers, EventCategoryWriteSerializers
from ..utilities.importbase import *

class eventcategoryViewsets(viewsets.ModelViewSet):
    serializer_class = EventCategoryListSerializers
    # permission_classes = [eventPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = EventCategory.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventCategoryWriteSerializers
        elif self.action == 'retrieve':
            return EventCategoryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

