from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Discipline
from ..serializers.discipline_serializers import DisciplineListSerializers, DisciplineRetrieveSerializers, DisciplineWriteSerializers
from ..utilities.importbase import *

class disciplineViewsets(viewsets.ModelViewSet):
    serializer_class = DisciplineListSerializers
    # permission_classes = [disciplinePermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Discipline.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DisciplineWriteSerializers
        elif self.action == 'retrieve':
            return DisciplineRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

